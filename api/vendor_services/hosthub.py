import requests
import os
import json
from ..utils import load_configuration, cents_to_eur_float

# Load environment variables
load_configuration()

HOSTHUB_KEY = os.getenv("HOSTHUB_KEY")
HOSTHUB_RENTAL_ID = os.getenv("HOSTHUB_RENTAL_ID")

class HostHubAPI:
    def __init__(self):
        self.base_url = "https://app.hosthub.com/api/2019-03-01"
        self.headers = {
            "Authorization": f"{HOSTHUB_KEY}",
            "Content-Type": "application/json"
        }

    def create_booking(self, date_from= "<date>", date_to= "<date>", metadata={}):
        url = f"{self.base_url}/rentals/{HOSTHUB_RENTAL_ID}/calendar-events"
        response = requests.post(url, headers=self.headers, data=json.dumps({
            "type": "Booking",
            "date_from": date_from,
            "date_to": date_to,
            # "source_id": "direct_stripe_checkout"
            **metadata
        }))

        if response.status_code == 200:
            return response.json()
        else:
            raise Exception(f"Error creating NEW booking: {response.text}")


    def update_booking(self, calendar_event_id, payment_data):

        # Normalize wrapper (sometimes callers pass {'payment_data': {...}})
        data = payment_data
        if isinstance(payment_data, dict) and 'payment_data' in payment_data and isinstance(payment_data['payment_data'], dict):
            data = payment_data['payment_data']

        # Extract common amount fields (all in cents)
        total_in_cents = data.get('amount') or data.get('amount_received')
        total_details = data.get('amount_details')
        tax_in_cents = data.get('amount_tax') or total_details.get('amount_tax') or 0

        # Prepare payload for HostHub. HostHub API schema isn't included here,
        # so send a clear `price_details` object plus some external references.
        payload = {
            "type": "Booking",
            "taxes": cents_to_eur_float(tax_in_cents),
            "total_payout": cents_to_eur_float(total_in_cents),
            "guest_paid": cents_to_eur_float(total_in_cents),
            "notes": json.dumps({
                "raw_payment_data": data,
                "derived": {
                    "payment_intent_id": data.get('id'),
                    "tax_cents": tax_in_cents,
                    "total_cents": total_in_cents
                }
            })
        }

        url = f"{self.base_url}/calendar-events/{calendar_event_id}"
        response = requests.post(url, headers=self.headers, data=json.dumps(payload))

        if response.status_code in (200, 201):
            return response.json()
        else:
            # Include payload in exception message (useful during development)
            raise Exception(f"Error updating booking: {response.status_code} - {response.text} - payload: {json.dumps(payload)}")

hosthub = HostHubAPI()
