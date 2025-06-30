from flask import Flask, request, Blueprint
from dotenv import load_dotenv
import stripe
import os
import logging
import json

# Load environment variables
load_dotenv()

# Configure Stripe API key
stripe.api_key = os.getenv('STRIPE_SECRET_KEY')

# Configure logging
logging.basicConfig(level=logging.INFO)

# Initialize Blueprint
blueprint = Blueprint("payment_webhooks", __name__)


@blueprint.route('/payment_event_callback', methods=['POST'])
def handle_webhook():
    event = None
    payload = request.data
    sig_header = request.headers['Stripe-Signature']
    secret = os.getenv('STRIPE_WEBHOOK_SECRET')

    try:
        # Verify the event came from Stripe
        event = stripe.Webhook.construct_event(
            payload=payload,
            sig_header=sig_header,
            secret=secret
        )
        logging.info(f'Webhook received: {event["type"]}')

        # Handle event types
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
            
            return 'Success', 200

            # Aquí puedes hacer: fulfill_order(session["id"])

    except ValueError as e:
        logging.error(f'❌ Invalid payload: {e}')
        return 'Invalid payload', 400
    except stripe.error.SignatureVerificationError as e:
        logging.error(f'❌ Invalid signature: {e}')
        return 'Invalid signature', 400
    except Exception as e:
        logging.error(f'❌ Unexpected error: {e}')
        return 'Internal server error', 500
    
    return 'Client Error', 400

 