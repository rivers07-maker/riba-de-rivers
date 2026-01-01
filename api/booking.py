from flask import request, redirect, Blueprint, jsonify
from dotenv import load_dotenv
from .vendor_services.hosthub import hosthub
from .rates import get_cached_rates
import stripe
import os
import logging
from datetime import datetime
from .utils import load_configuration

# Initialize Blueprint
blueprint = Blueprint("booking", __name__, template_folder='../public')

# Load environment variables
load_configuration()

# Configure logging
logging.basicConfig(level=logging.INFO)

# Stripe API key
stripe.api_key = os.getenv("STRIPE_SECRET_KEY")

@blueprint.route('/process_booking_payment', methods=['POST'])
def process_booking_payment():
    try:
        # Fetch current rates and settings from Hosthub (cached)
        rates = get_cached_rates()
        PRICE_PER_NIGHT_FLOAT = rates.get('nightly_rate', 65.0)
        PRICE_PER_CLEANING_FLOAT = rates.get('cleaning_fee', 25.0)
        PRICE_PER_PETS_FLOAT = rates.get('pet_fee', 10.0)
        EXTRA_PERSON_FEE_FLOAT = rates.get('extra_person_fee', 10.0)
        EXTRA_PERSON_THRESHOLD = rates.get('extra_person_threshold', 2)

        # Convert to cents for Stripe
        PRICE_PER_NIGHT = int(PRICE_PER_NIGHT_FLOAT * 100)
        PRICE_PER_CLEANING = int(PRICE_PER_CLEANING_FLOAT * 100)
        PRICE_PER_PETS = int(PRICE_PER_PETS_FLOAT * 100)
        EXTRA_PERSON_FEE = int(EXTRA_PERSON_FEE_FLOAT * 100)

        # Extract form data
        arrival = request.form.get('arrival')
        departure = request.form.get('departure')
        name = request.form.get('name')
        phone = request.form.get('phone')
        email = request.form.get('email')

        # Check for missing required fields
        if not all([arrival, departure, name, phone, email]):
            return jsonify({"error": "Missing required fields"}), 400

        # Parse and validate dates
        try:
            arrival_date = datetime.strptime(arrival, '%d/%m/%Y')
            departure_date = datetime.strptime(departure, '%d/%m/%Y')
        except ValueError:
            return jsonify({"error": "Invalid date format. Use DD/MM/YYYY."}), 400

        # Calculate number of nights
        nights = (departure_date - arrival_date).days
        if nights < 1:
            return jsonify({"error": "Invalid number of nights"}), 400

        # Extract additional data from guests and pets form
        try:
            adults = int(request.form.get('adults', 1))
            children = int(request.form.get('children', 0))
            pets = int(request.form.get('pets', 0))
        except ValueError:
            return jsonify({"error": "Invalid input: adults, children, and pets must be numbers."}), 400

        # Set whether to include cleaning fee
        include_cleaning = True

        # Log extracted data
        logging.info(f"Booking details: Arrival - {arrival_date}, Departure - {departure_date}, Nights - {nights}")
        logging.info(f"Guests: Adults - {adults}, Children - {children}, Pets - {pets}, Cleaning - {include_cleaning}")

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
            extra_fees += (EXTRA_PERSON_FEE * extra_guests)

        # Calculate total price: (nightly price * nights) + extras
        total_amount = (PRICE_PER_NIGHT * nights) + extra_fees

        # Also compute booking_value (nightly subtotal without extras)
        booking_value = PRICE_PER_NIGHT * nights

        # Create a single line item with the total amount
        line_items = [{
            'price_data': {
                'currency': 'eur',
                'product_data': {
                    'name': 'Reservation',
                    'description': f"{name} - {nights} night(s) stay from {arrival} to {departure}",
                    'images': ['https://riba-de-rivers.vercel.app/assets/images/overview.jpg'],
                },
                'unit_amount': total_amount,
            },
            'quantity': 1
        }]

        default_metadata = {
            'guest_name': name,
            'guest_adults': adults,
            'guest_children': children,
            'guest_email': email,
            'guest_phone': phone,
            'booking_value': cents_to_eur_float(booking_value),
            'cleaning_fee': cents_to_eur_float(PRICE_PER_CLEANING if include_cleaning else 0),
            'other_fees': cents_to_eur_float(extra_fees - (PRICE_PER_CLEANING if include_cleaning else 0)),
            'currency': 'eur'
        }

        # Ahora, registra el valor en centavos para verificar.
        logging.info(f"Metadata Fees (in cents): Booking Value - {default_metadata['booking_value']['cents']}, Cleaning Fee - {default_metadata['cleaning_fee']['cents']}, Other Fees - {default_metadata['other_fees']['cents']}")

        # Create booking in HostHub
        created_booking_response = hosthub.create_booking(date_from=arrival_date.date().isoformat(),
                                                          date_to=departure_date.date().isoformat(),
                                                          metadata=default_metadata)

        logging.info(f"Booking Created! Booking Response: {created_booking_response}")

        # Create Stripe Checkout session
        session = stripe.checkout.Session.create(
            payment_method_types=['card'],
            line_items=line_items,
            mode='payment',
            success_url='https://riba-de-rivers.vercel.app/index.html',
            cancel_url='https://riba-de-rivers.vercel.app/contact.html',
            customer_email=email,
            payment_intent_data={
                'metadata': {
                    'reservation_id': created_booking_response.get('reservation_id'),
                    'calendar_event_id': created_booking_response.get('id'),
                    'arrival_date': arrival,
                    'departure_date': departure,
                }
            },
            metadata={
                # Stripe NO acepta diccionarios/hashes en los valores de metadata.
                # Debemos convertir los valores de tarifa de HostHub a strings.
                'guest_name': name,
                'guest_adults': str(adults),
                'guest_children': str(children),
                'guest_email': email,
                'guest_phone': phone,
                'booking_value': str(booking_value), # Usamos el valor en centavos como string
                'cleaning_fee': str(PRICE_PER_CLEANING if include_cleaning else 0), # Centavos como string
                'other_fees': str(PRICE_PER_PETS if pets > 0 else 0), # Centavos como string

                
                'nights': str(nights),
                'pets': str(pets),
                'total_amount': str(total_amount), # Total en centavos como string
            }
        )

        return redirect(session.url)

    except Exception as e:
        logging.error(f"Error processing booking payment: {e}")
        return jsonify({"error": "Internal Server Error"}), 500
