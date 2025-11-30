import requests
import os
import json
import logging
from ..utils import load_configuration, parse_date
from datetime import datetime

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger("HostHubAPI")

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

    def create_booking(self, date_from="<date>", date_to="<date>", metadata={}):
        url = f"{self.base_url}/rentals/{HOSTHUB_RENTAL_ID}/calendar-events"
        payload = {
            "type": "Booking",
            "date_from": date_from,
            "date_to": date_to,
            **metadata
        }
        
        # Only log the date range, not the full metadata
        logger.info(f"Creating booking from {date_from} to {date_to}")
        
        response = requests.post(url, headers=self.headers, data=json.dumps(payload))

        if response.status_code == 200:
            logger.info("Booking created successfully.")
            return response.json()
        else:
            logger.error(f"Failed to create booking. Status: {response.status_code}, Response: {response.text}")
            raise Exception(f"Error creating NEW booking: {response.text}")

    def update_booking(self, calendar_event_id, payment_data):
        logger.info(f"Starting update_booking for Event ID: {calendar_event_id}")
        data = payment_data
        if isinstance(payment_data, dict) and 'payment_data' in payment_data and isinstance(payment_data['payment_data'], dict):
            data = payment_data['payment_data']

        total_in_cents = data.get('amount') or data.get('amount_received')
        try:
            total_payout_cents = int(total_in_cents) if total_in_cents is not None else 0
            guest_paid_cents = int(total_in_cents) if total_in_cents is not None else 0
        except (ValueError, TypeError) as e:
            logger.warning(f"Error converting amount to int: {total_in_cents}. Defaulting to 0. Error: {e}")
            total_payout_cents = 0
            guest_paid_cents = 0

        metadata = data.get('metadata', {})
        arrival = metadata.get('arrival_date')
        departure = metadata.get('departure_date')
        date_from_iso = parse_date(arrival)
        date_to_iso = parse_date(departure)

        if not date_from_iso or not date_to_iso:
            logger.warning(f"MISSING DATES for Event ID {calendar_event_id}. Parsed: {date_from_iso} / {date_to_iso}")

        notes_data = {
            "payment_intent_id": data.get('id'),
            "total_cents": total_in_cents,
            "raw_payment_data": data
        }
        notes_str = HostHubAPI.format_payment_notes(notes_data)
        payload = {
            "type": "Booking",
            "total_payout": {
                'cents': total_payout_cents,
                'currency': 'EUR'
            },
            "guest_paid": {
                'cents': guest_paid_cents,
                'currency': 'EUR'
            },
            "notes": notes_str
        }
        if date_from_iso:
            payload["date_from"] = date_from_iso
        if date_to_iso:
            payload["date_to"] = date_to_iso

        url = f"{self.base_url}/calendar-events/{calendar_event_id}"
        try:
            response = requests.post(url, headers=self.headers, data=json.dumps(payload))
            if response.status_code in (200, 201):
                logger.info(f"Successfully updated booking {calendar_event_id}")
                return response.json()
            else:
                is_html_error = response.status_code >= 500 and "<html" in response.text.lower()
                error_preview = "Server Error (HTML Content)" if is_html_error else response.text
                logger.error(f"HostHub API Error {response.status_code}: {error_preview}")
                raise Exception(f"Error updating booking: {response.status_code} - {error_preview}")
        except requests.RequestException as e:
            logger.critical(f"Network error connecting to HostHub: {e}")
            raise
        
    @staticmethod
    def format_payment_notes(data):
        """
        Formats the payment data for the Hosthub UI.
        Receives a dict with key fields and returns a presentable string.
        """
        # Allows for both flat dict and nested dict (raw/derived)
        raw = data.get('raw_payment_data', data)
        derived = data.get('derived', data)
        
        # Payment ID extraction
        payment_id = derived.get('payment_intent_id') or raw.get('id') or '-'
        # Amount calculation
        total_cents = derived.get('total_cents') or raw.get('amount') or 0
        total_eur = f"€{int(total_cents)/100:.2f}" if total_cents else "-"
        # Status determination
        succeeded = raw.get('status') == 'succeeded'
        status = "Successful" if succeeded else "Failed"
        # Method determination
        method = raw.get('payment_method_types', ['-'])
        method_str = method[0].capitalize() if isinstance(method, list) and method else str(method).capitalize()
        # Date determination and formatting
        date_ts = raw.get('created')
        if date_ts:
            try:
                date_str = datetime.utcfromtimestamp(int(date_ts)).strftime('%d/%m/%Y')
            except Exception:
                date_str = str(date_ts)
        else:
            date_str = "-"
            
        # Returning the formatted string
        return (
            f"Stripe Payment | Payment ID: {payment_id} | Amount: {total_eur} | Status: {status} | Method: {method_str} | Date: {date_str}"
        )

hosthub = HostHubAPI()