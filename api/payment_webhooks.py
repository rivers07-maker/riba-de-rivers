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
    payload = request.get_data()
    
    try:
        event = stripe.Webhook.construct_event(
            payload=payload,
            sig_header=request.headers['Stripe-Signature'],
            secret=os.getenv('STRIPE_SECRET_KEY')
        )
        
        if event.type == 'checkout.session.completed':
            # fulfill_order(event.data.object.id)
            logging.info('Test webhook received')
            
    except ValueError as e:
        return 'Invalid payload', 400
    except stripe.error.SignatureVerificationError as e:
        return 'Invalid signature', 400
        
    return 'Success', 200