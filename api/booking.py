from flask import request, redirect, render_template, Blueprint, jsonify
from dotenv import load_dotenv
import stripe
import os
import logging

blueprint = Blueprint("booking", __name__, template_folder='../public')

load_dotenv()

# Stripe API key
stripe.api_key = os.getenv("STRIPE_SECRET_KEY")

# Define the price per night (65 EUR)
PRICE_PER_NIGHT = 65 * 100  # Convert to cents (Stripe uses cents)
PRICE_PER_CLEANING = 50 * 100  # Convert to cents (Stripe uses cents)
PRICE_PER_PETS = 20 * 100  # Convert to cents (Stripe uses cents)

# Configure logging
logging.basicConfig(level=logging.DEBUG)


@blueprint.route('/process-booking-payment', methods=['POST'])
def process_booking_payment():
    try:
        arrival= request.form.get('arrival')
        print(arrival)

    except Exception as e:
        logging.error(f"Error processing booking payment: {e}")

        
    
