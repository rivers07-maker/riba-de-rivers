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

            temporary_booking_response = hosthub.create_temporary_booking(type="Hold", date_from=arrival_date.date().isoformat(), date_to=departure_date.date().isoformat())
            print(temporary_booking_response)

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

        # Create Stripe Checkout session
        session = stripe.checkout.Session.create(
            payment_method_types=['card'],
            line_items=line_items,
            mode='payment',
            success_url='https://riba-de-rivers.vercel.app/index.html',
            cancel_url='https://riba-de-rivers.vercel.app/contact.html',
            customer_email=email,
            metadata={
                'guest_name': name,
                'guest_phone': phone,
                'guest_email': email,
                'arrival_date': arrival,
                'departure_date': departure,
                'nights': nights,
                'adults': adults,
                'children': children,
                'pets': pets,
            }
        )

        print(session)

        return redirect(session.url)

    except Exception as e:
        logging.error(f"Error processing booking payment: {e}")
        return jsonify({"error": "Internal Server Error"}), 500
