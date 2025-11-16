import requests
import os
import json
import logging
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
            raise Exception(f"Error creating temporary booking: {response.text}")



    def update_booking(self, calendar_event_id, payment_data):

        # Normalize wrapper (sometimes callers pass {'payment_data': {...}})
        data = payment_data
        if isinstance(payment_data, dict) and 'payment_data' in payment_data and isinstance(payment_data['payment_data'], dict):
            data = payment_data['payment_data']


        # Extract common amount fields (all in cents)
        total_in_cents = data.get('amount') or data.get('amount_received')
        total_details = data.get('amount_details')
        tax_in_cents = data.get('amount_tax') or (total_details.get('amount_tax') if total_details else 0) or 0

        # Extra: Try to extract breakdown if present in metadata
        metadata = (data.get('metadata') or {}) if isinstance(data, dict) else {}
        booking_value = metadata.get('booking_value')
        cleaning_fee = metadata.get('cleaning_fee')
        other_fees = metadata.get('other_fees')

        # Logging info for traceability
        logging.info(f"Hosthub update_booking: booking_value={booking_value}, cleaning_fee={cleaning_fee}, other_fees={other_fees}")


        # Prepare payload for HostHub
        payload = {
            "type": "Booking",
            "taxes": cents_to_eur_float(tax_in_cents),
            "total_payout": cents_to_eur_float(total_in_cents),
            "guest_paid": cents_to_eur_float(total_in_cents),
            "booking_value": cents_to_eur_float(int(booking_value)) if booking_value else None,
            "cleaning_fee": cents_to_eur_float(int(cleaning_fee)) if cleaning_fee else None,
            "other_fees": cents_to_eur_float(int(other_fees)) if other_fees else None,
            "notes": json.dumps({
                "raw_payment_data": data,
                "derived": {
                    "payment_intent_id": data.get('id'),
                    "tax_cents": tax_in_cents,
                    "total_cents": total_in_cents,
                    "booking_value": booking_value,
                    "cleaning_fee": cleaning_fee,
                    "other_fees": other_fees
                }
            })
        }

        url = f"{self.base_url}/calendar-events/{calendar_event_id}"
        try:
            response = requests.post(url, headers=self.headers, data=json.dumps(payload))
            if response.status_code in (200, 201):
                return response.json()
            else:
                logging.error(f"Error updating booking: {response.status_code} - {response.text} - payload: {json.dumps(payload)}")
                raise Exception(f"Error updating booking: {response.status_code} - {response.text} - payload: {json.dumps(payload)}")
        except Exception as e:
            logging.error(f"Exception in update_booking: {e}")
            raise

hosthub = HostHubAPI()
