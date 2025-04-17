from flask import request, redirect, Blueprint, jsonify
from dotenv import load_dotenv
import stripe
import os
import logging
from datetime import datetime

# Initialize Blueprint
blueprint = Blueprint("booking", __name__, template_folder='../public')

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO)

# Stripe API key
stripe.api_key = os.getenv("STRIPE_SECRET_KEY")

# Constants (in cents)
PRICE_PER_NIGHT = 65 * 100  # 65 EUR per night
PRICE_PER_CLEANING = 50 * 100  # Optional cleaning fee
PRICE_PER_PETS = 20 * 100  # Optional pet fee

@blueprint.route('/process-booking-payment', methods=['POST'])
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

        include_cleaning = True

        # Log extracted data
        logging.info(f"Booking details: Arrival - {arrival_date}, Departure - {departure_date}, Nights - {nights}")
        logging.info(f"Guests: Adults - {adults}, Children - {children}, Pets - {pets}, Cleaning - {include_cleaning}")

        # Calculate line items based on booking details
        line_items = [{
            'price_data': {
                'currency': 'eur',
                'product_data': {
                    'name': 'Reservation',
                    'description': f"{name} - {nights} night(s) stay from {arrival} to {departure}",
                    'images': ['../assets/images/hero.jpg'],  # Replace with actual image URL
                },
                'unit_amount': PRICE_PER_NIGHT,
            },
            'quantity': nights
        }]

        # Add cleaning fee if selected
        if include_cleaning:
            line_items.append({
                'price_data': {
                    'currency': 'eur',
                    'product_data': { 'name': 'Cleaning Fee' },
                    'unit_amount': PRICE_PER_CLEANING,
                },
                'quantity': 1
            })

        # Add pet fee if pets are selected
        if pets > 0:
            line_items.append({
                'price_data': {
                    'currency': 'eur',
                    'product_data': { 'name': 'Pet Fee' },
                    'unit_amount': PRICE_PER_PETS,
                },
                'quantity': pets
            })

        # Create Stripe Checkout session
        session = stripe.checkout.Session.create(
            payment_method_types=['card'],
            line_items=line_items,
            mode='payment',
            success_url='https://yourdomain.com/success',
            cancel_url='https://yourdomain.com/cancel',
            customer_email=email,  # Send customer email to Stripe
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

        # Redirect user to Stripe Checkout
        return redirect(session.url)

    except Exception as e:
        logging.error(f"Error processing booking payment: {e}")
        return jsonify({"error": "Internal Server Error"}), 500


        
    
