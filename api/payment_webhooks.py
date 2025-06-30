from flask import Flask, request, Blueprint
from dotenv import load_dotenv
import stripe
import os
import logging
import json

# Initialize Blueprint
blueprint = Blueprint("payment_webhooks", __name__)

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO)

@blueprint.route('/payment_event_callback', methods=['POST'])
def handle_webhook():
    event = None
    payload = request.data
    sig_header = request.headers['Stripe-Signature']
    secret = os.getenv('STRIPE_SECRET_KEY')

    try:
        event = stripe.Webhook.construct_event(payload, sig_header, secret)
        logging.info(f'Event: {event}')
        
        if event['type'] == 'checkout.session.completed':
            session = event['data']['object']

            print("\n=== Checkout Session ===")
            print(f"Payment Intent ID: {session.payment_intent}")
            
            # Retrieve the Payment Intent with expanded fields
            print("\n=== Retrieving Payment Intent ===")
            payment_intent = stripe.PaymentIntent.retrieve(session.payment_intent)
            print("Full Payment Intent:")
            print(payment_intent)
            
            # Check metadata specifically
            print("\n=== Metadata Check ===")
            if 'metadata' in payment_intent:
                print("Metadata exists:")
                print(payment_intent.metadata)
            else:
                print("No metadata found")
            
            logging.info(f'✅ Payment completed for session ID: {session["id"]}')
            
    except ValueError as e:
        logging.error(f'ValueError: {e}')
        return 'Invalid payload', 400
    except stripe.error.SignatureVerificationError as e:
        return 'Invalid signature', 400
    except Exception as e:
        logging.error(f'Error: {e}')
        return 'Internal server error', 500
    return 'Success', 200