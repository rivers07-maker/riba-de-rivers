from flask import request, redirect, Blueprint, jsonify
from dotenv import load_dotenv
from .vendor_services.hosthub import hosthub
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

# Constants (in cents)
PRICE_PER_NIGHT = 65 * 100  # 65 EUR per night
PRICE_PER_CLEANING = 50 * 100  # Mandatory cleaning fee
PRICE_PER_PETS = 20 * 100  # Optional pet fee

@blueprint.route('/process_booking_payment', methods=['POST'])
def process_booking_payment():
    try:
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

        # Set whether to include cleaning fee (you can later change this to be conditional)
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
                    'images': ['https://riba-de-rivers.vercel.app/assets/images/overview.jpg'],  # Replace with actual image URL
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
            # --- Implementación del Objeto (Money) ---
            # HostHub espera un objeto con 'cents' (entero) y 'currency' (string)
            'booking_value': {
                'cents': booking_value, # booking_value ya está en centavos (entero)
                'currency': 'EUR'
            },
            'cleaning_fee': {
                'cents': PRICE_PER_CLEANING if include_cleaning else 0,
                'currency': 'EUR'
            },
            'other_fees': {
                'cents': PRICE_PER_PETS if pets > 0 else 0,
                'currency': 'EUR'
            }
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
            # Put an explicit breakdown into both the payment_intent metadata and
            # top-level session metadata.
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

        print(session)

        return redirect(session.url)

    except Exception as e:
        logging.error(f"Error processing booking payment: {e}")
        return jsonify({"error": "Internal Server Error"}), 500
