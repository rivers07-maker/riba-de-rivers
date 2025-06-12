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
    payload = request.get_json() if request.is_json else json.loads(request.data)
    sig_header = request.headers['Stripe-Signature']
    secret = os.getenv('STRIPE_SECRET_KEY')

    try:
        event = stripe.Webhook.construct_event(payload, sig_header, secret)
        logging.info(f'Event: {event}')
        
        if event['type'] == 'checkout.session.completed':
            # fulfill_order(event.data.object.id)
            logging.info('Test webhook received')
            
    except ValueError as e:
        logging.error(f'ValueError: {e}')
        return 'Invalid payload', 400
    except stripe.error.SignatureVerificationError as e:
        return 'Invalid signature', 400
    except Exception as e:
        logging.error(f'Error: {e}')
        return 'Internal server error', 500
    return 'Success', 200