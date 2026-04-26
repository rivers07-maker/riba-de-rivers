from flask import request, redirect, Blueprint, jsonify
from dotenv import load_dotenv
from .vendor_services.hosthub import hosthub
from .rates import get_cached_rates
import stripe
import os
import logging
from supabase import create_client, Client
import logging
from datetime import datetime
from .utils import load_configuration, cents_to_eur_float

# Initialize Blueprint
blueprint = Blueprint("booking", __name__, template_folder="../public")

# Load environment variables
load_configuration()

# Configure logging
logging.basicConfig(level=logging.INFO)

# Stripe API key
stripe.api_key = os.getenv("STRIPE_SECRET_KEY")

# Supabase credentials
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

try:
    supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)
except Exception as e:
    logging.error(f"Error creating Supabase client for booking: {e}")
    supabase = None

@blueprint.route("/process_booking_payment", methods=["POST"])
def process_booking_payment():
    try:
        # Fetch current rates and settings from Hosthub (cached)
        rates = get_cached_rates()
        PRICE_PER_NIGHT_FLOAT = rates.get("nightly_rate", 65.0)
        PRICE_PER_CLEANING_FLOAT = rates.get("cleaning_fee", 25.0)
        PRICE_PER_PETS_FLOAT = rates.get("pet_fee", 10.0)
        EXTRA_PERSON_FEE_FLOAT = rates.get("extra_person_fee", 10.0)
        EXTRA_PERSON_THRESHOLD = rates.get("extra_person_threshold", 2)
        MIN_STAY = rates.get("min_stay", 2)

        # Convert to cents for Stripe
        PRICE_PER_NIGHT = int(PRICE_PER_NIGHT_FLOAT * 100)
        PRICE_PER_CLEANING = int(PRICE_PER_CLEANING_FLOAT * 100)
        PRICE_PER_PETS = int(PRICE_PER_PETS_FLOAT * 100)
        EXTRA_PERSON_FEE = int(EXTRA_PERSON_FEE_FLOAT * 100)

        # Extract form data
        arrival = request.form.get("arrival")
        departure = request.form.get("departure")
        name = request.form.get("name")
        phone = request.form.get("phone")
        email = request.form.get("email")
        coupon_code = request.form.get("coupon_code", "").strip().upper()

        # Check for missing required fields
        if not all([arrival, departure, name, phone, email]):
            return jsonify({"error": "Missing required fields"}), 400

        # Parse and validate dates
        try:
            arrival_date = datetime.strptime(arrival, "%d/%m/%Y")
            departure_date = datetime.strptime(departure, "%d/%m/%Y")
        except ValueError:
            return jsonify({"error": "Invalid date format. Use DD/MM/YYYY."}), 400

        # Calculate number of nights
        nights = (departure_date - arrival_date).days
        if nights < MIN_STAY:
            return jsonify({"error": f"Minimum stay is {MIN_STAY} nights"}), 400

        # Extract additional data from guests and pets form
        try:
            adults = int(request.form.get("adults", 1))
            children = int(request.form.get("children", 0))
            pets = int(request.form.get("pets", 0))
        except ValueError:
            return jsonify(
                {"error": "Invalid input: adults, children, and pets must be numbers."}
            ), 400

        # Set whether to include cleaning fee
        include_cleaning = True

        # Log extracted data
        logging.info(
            f"Booking details: Arrival - {arrival_date}, Departure - {departure_date}, Nights - {nights}"
        )
        logging.info(f"Guests: Adults - {adults}, Children - {children}, Pets - {pets}")

        # Calculate extra fees
        extra_fees = 0
        if include_cleaning:
            extra_fees += PRICE_PER_CLEANING
        if pets > 0:
            extra_fees += PRICE_PER_PETS

        # Calculate extra person fees
        total_guests = adults + children
        if total_guests > EXTRA_PERSON_THRESHOLD:
            extra_guests = total_guests - EXTRA_PERSON_THRESHOLD
            extra_fees += EXTRA_PERSON_FEE * extra_guests

        # Calculate total price (cents)
        total_amount = (PRICE_PER_NIGHT * nights) + extra_fees
        booking_value = PRICE_PER_NIGHT * nights
        
        # Coupon Handling
        discount_percent = 0
        discount_amount = 0
        original_total = total_amount

        if coupon_code and supabase:
            try:
                response = supabase.table("cupones").select("descuento, activo, expiracion").eq("codigo", coupon_code).execute()
                if response.data and len(response.data) > 0:
                    coupon = response.data[0]
                    
                    expiration = coupon.get("expiracion")
                    if expiration and expiration < datetime.today().date().isoformat():
                        logging.info(f"Coupon {coupon_code} exists but has expired on {expiration}")
                        coupon_code = "" # invalid coupon
                    elif coupon.get("activo"):
                        desc = coupon.get("descuento", 0)
                        if 1 <= desc <= 100:
                            discount_percent = desc
                            discount_amount = int(original_total * (discount_percent / 100))
                            total_amount = original_total - discount_amount
                            logging.info(f"Validated coupon {coupon_code}: {discount_percent}% off ({discount_amount} cents). New total: {total_amount} cents.")
                        else:
                            logging.warning(f"Coupon {coupon_code} applied but has invalid discount value: {desc}")
                            coupon_code = "" # invalid coupon

                    else:
                        logging.info(f"Coupon {coupon_code} is inactive")
                        coupon_code = "" # invalid coupon
                else:
                    logging.info(f"Coupon {coupon_code} not found")
                    coupon_code = "" # invalid coupon
            except Exception as e:
                logging.error(f"Error checking coupon {coupon_code} in booking: {e}")
                coupon_code = "" # invalid coupon

        # Create Hosthub Metadata
        # We avoid sending custom fee fields in the root as it causes 400 errors from Hosthub API
        hosthub_metadata = {
            "guest_name": name,
            "guest_adults": str(adults),
            "guest_children": str(children),
            "guest_email": email,
            "guest_phone": phone,
            "currency": "EUR",
        }

        logging.info("Calling hosthub.create_booking...")
        # Create booking in HostHub
        created_booking_response = hosthub.create_booking(
            date_from=arrival_date.date().isoformat(),
            date_to=departure_date.date().isoformat(),
            metadata=hosthub_metadata,
        )

        logging.info(f"Booking Created! ID: {created_booking_response.get('id')}")

        # Create Stripe Checkout session
        session = stripe.checkout.Session.create(
            payment_method_types=["card"],
            line_items=[
                {
                    "price_data": {
                        "currency": "eur",
                        "product_data": {
                            "name": "Reservation",
                            "description": f"{name} - {nights} night(s) stay from {arrival} to {departure}",
                            "images": [
                                "https://riba-de-rivers.vercel.app/assets/images/overview.jpg"
                            ],
                        },
                        "unit_amount": total_amount,
                    },
                    "quantity": 1,
                }
            ],
            mode="payment",
            success_url="https://riba-de-rivers.vercel.app/index.html",
            cancel_url="https://riba-de-rivers.vercel.app/contact.html",
            customer_email=email,
            payment_intent_data={
                "metadata": {
                    # Hosthub API returns 'id' which serves as the unique identifier for the event/reservation
                    # In some contexts, reservation_id might be distinct or the same, but we need ensuring we capture it.
                    # Based on successful create logs, we have an ID like 'QPjXy2KbN0'.
                    "reservation_id": created_booking_response.get("reservation_id")
                    or created_booking_response.get("id", ""),
                    "calendar_event_id": created_booking_response.get("id", ""),
                    "arrival_date": arrival,
                    "departure_date": departure,
                    # Include guest details here so the webhook can find them in the PaymentIntent
                    "guest_name": name,
                    "guest_adults": str(adults),
                    "guest_children": str(children),
                    "guest_email": email,
                    "guest_phone": phone,
                    "booking_value_eur": f"{cents_to_eur_float(booking_value):.2f}",
                    "cleaning_fee_eur": f"{cents_to_eur_float(PRICE_PER_CLEANING if include_cleaning else 0):.2f}",
                    "other_fees_eur": f"{cents_to_eur_float(extra_fees - (PRICE_PER_CLEANING if include_cleaning else 0)):.2f}",
                    "total_amount_eur": f"{cents_to_eur_float(total_amount):.2f}",
                    "original_total_eur": f"{cents_to_eur_float(original_total):.2f}",
                    "discount_percent": str(discount_percent),
                    "discount_amount_eur": f"{cents_to_eur_float(discount_amount):.2f}",
                    "coupon_code": coupon_code,
                    # Values in cents for the Hosthub update_booking payload
                    "booking_value_cents": str(booking_value),
                    "cleaning_fee_cents": str(
                        PRICE_PER_CLEANING if include_cleaning else 0
                    ),
                    "other_fees_cents": str(
                        extra_fees - (PRICE_PER_CLEANING if include_cleaning else 0)
                    ),
                    "total_amount_cents": str(total_amount),
                    "nights": str(nights),
                    "pets": str(pets),
                }
            },
            metadata={
                # Duplicate for the Session object just in case, though webhook uses PaymentIntent
                "guest_name": name,
                "guest_email": email,
                "calendar_event_id": created_booking_response.get("id", ""),
                "total_amount_eur": f"{cents_to_eur_float(total_amount):.2f}",
            },
        )

        return redirect(session.url)

    except Exception as e:
        logging.error(f"Error processing booking payment: {e}")
        return jsonify({"error": "Internal Server Error"}), 500
