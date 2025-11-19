import requests
import os
import json
import logging
from ..utils import load_configuration
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
        
        logger.info(f"Creating booking: {date_from} to {date_to}")
        
        response = requests.post(url, headers=self.headers, data=json.dumps(payload))

        if response.status_code == 200:
            logger.info("Booking created successfully.")
            return response.json()
        else:
            logger.error(f"Failed to create booking. Status: {response.status_code}, Response: {response.text}")
            raise Exception(f"Error creating NEW booking: {response.text}")

    def _parse_date(self, date_str):
        """Helper para intentar parsear la fecha con múltiples formatos"""
        if not date_str:
            return None
        
        formats = ['%d/%m/%Y', '%Y-%m-%d', '%Y/%m/%d']
        for fmt in formats:
            try:
                return datetime.strptime(date_str, fmt).date().isoformat()
            except ValueError:
                continue
        return None

    def update_booking(self, calendar_event_id, payment_data):
        logger.info(f"--- Starting update_booking for Event ID: {calendar_event_id} ---")
        
        # Normalize wrapper
        data = payment_data
        if isinstance(payment_data, dict) and 'payment_data' in payment_data and isinstance(payment_data['payment_data'], dict):
            data = payment_data['payment_data']

        # Extract common amount fields
        total_in_cents = data.get('amount') or data.get('amount_received')

        # --- Manejo de la estructura de dinero ---
        try:
            total_payout_cents = int(total_in_cents) if total_in_cents is not None else 0
            guest_paid_cents = int(total_in_cents) if total_in_cents is not None else 0
        except (ValueError, TypeError) as e:
            logger.warning(f"Error converting amount to int: {total_in_cents}. Defaulting to 0. Error: {e}")
            total_payout_cents = 0
            guest_paid_cents = 0

        # --- Extracción y formateo de fechas ---
        metadata = data.get('metadata', {})
        arrival = metadata.get('arrival_date')
        departure = metadata.get('departure_date')
        
        date_from_iso = self._parse_date(arrival)
        date_to_iso = self._parse_date(departure)

        # Log de advertencia si faltan fechas, ya que esto suele causar el error 500 en HostHub
        if not date_from_iso or not date_to_iso:
            logger.warning(f"MISSING DATES: Arrival raw: '{arrival}', Departure raw: '{departure}'. Parsed: {date_from_iso} / {date_to_iso}")

        # --- Prepare payload for HostHub ---
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
            "notes": json.dumps({
                "raw_payment_data": data,
                "derived": {
                    "payment_intent_id": data.get('id'),
                    "total_cents": total_in_cents
                }
            })
        }
        
        # --- Añadir fechas solo si son válidas ---
        if date_from_iso:
            payload["date_from"] = date_from_iso
        if date_to_iso:
            payload["date_to"] = date_to_iso

        # Log del payload completo para depuración (útil para ver qué estamos enviando exactamente)
        logger.info(f"Payload prepared for HostHub: {json.dumps(payload)}")

        url = f"{self.base_url}/calendar-events/{calendar_event_id}"
        
        try:
            response = requests.post(url, headers=self.headers, data=json.dumps(payload))
            
            if response.status_code in (200, 201):
                logger.info(f"Successfully updated booking {calendar_event_id}")
                return response.json()
            else:
                # Detectar si es el error HTML gigante (500) para limpiar el log
                is_html_error = response.status_code >= 500 and "<html" in response.text.lower()
                error_preview = "Server Error (HTML Content)" if is_html_error else response.text
                
                logger.error(f"HostHub API Error {response.status_code}: {error_preview}")
                logger.error(f"Failed Payload was: {json.dumps(payload)}")
                
                raise Exception(f"Error updating booking: {response.status_code} - {error_preview}")
                
        except requests.RequestException as e:
            logger.critical(f"Network error connecting to HostHub: {e}")
            raise

hosthub = HostHubAPI()