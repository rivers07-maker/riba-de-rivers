from flask import Flask, request, Blueprint
from dotenv import load_dotenv
import stripe
import os
import logging
import json
from .vendor_services.hosthub import hosthub

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
    secret = os.getenv('STRIPE_WEBHOOK_SECRET')

    try:
        event = stripe.Webhook.construct_event(payload, sig_header, secret)
        logging.info(f'Event: {event}')
        
        if event['type'] == 'checkout.session.completed':
            session = event['data']['object']
            
            payment_intent = stripe.PaymentIntent.retrieve(session.payment_intent)
            
            try:
                if 'metadata' not in payment_intent:
                    logging.error("No payment intent metadata found")
                    raise Exception("No payment intent metadata found")
                #Si se rompe en esta linea quiere decir que no le estoy pasando en booking.py la metadata correcta en las linea 106-110
            
                #Pasar el payment session ID a Hosthub
                hosthub.update_booking(payment_intent['metadata']['calendar_event_id'], payment_intent)
            except Exception as e:
                logging.error(f'Error updating booking in HostHub: {e}')
                #Si se rompe en esta linea quiere decir que hubo un error con Hosthub
                return 'Internal server error', 500
            
    except ValueError as e:
        logging.error(f'ValueError: {e}')
        return 'Invalid payload', 400
    except stripe.error.SignatureVerificationError as e:
        return 'The cause of the error is Invalid Signature from Stripe', 400
    except Exception as e:
        logging.error(f'Error: {e}')
        return 'Internal server error', 500
    return 'Success', 200