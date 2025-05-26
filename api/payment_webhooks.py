from flask import Flask, request, Blueprint
from dotenv import load_dotenv
import stripe
import os
import logging


# Initialize Blueprint
blueprint = Blueprint("payment_webhooks", __name__)

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO)

@blueprint.route('/payment_event_callback', methods=['POST'])
def handle_webhook():
    event = None
    payload = request.get_json()
    logging.info(f'Payload: {payload}')
    logging.info(f'Headers: {request.headers}')
    logging.info(f'Body: {request.get_json()}')

    try:
        event = stripe.Webhook.construct_event(
            payload=payload,
            sig_header=request.headers['Stripe-Signature'],
            secret=os.getenv('STRIPE_SECRET_KEY')
        )
        logging.info(f'Event: {event}')
        
        if event.type == 'checkout.session.completed':
            # fulfill_order(event.data.object.id)
            logging.info('Test webhook received')
            
    except ValueError as e:
        return 'Invalid payload', 400
    except stripe.error.SignatureVerificationError as e:
        return 'Invalid signature', 400
    except Exception as e:
        logging.error(f'Error: {e}')
        return 'Internal server error', 500
    return 'Success', 200