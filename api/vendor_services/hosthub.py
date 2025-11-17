import requests
import os
import json
from ..utils import load_configuration
from datetime import datetime

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
        tax_in_cents = data.get('amount_tax') or (total_details.get('amount_tax') if total_details else 0) or 0
        
        # --- NUEVA LÓGICA: Extraer y formatear fechas de la metadata de Stripe ---
        metadata = data.get('metadata', {})
        date_from_iso = None
        date_to_iso = None

        arrival = metadata.get('arrival_date')
        departure = metadata.get('departure_date')
        
        if arrival and departure:
            try:
                # Stripe almacena 'DD/MM/YYYY', HostHub espera 'YYYY-MM-DD'
                date_from_iso = datetime.strptime(arrival, '%d/%m/%Y').date().isoformat()
                date_to_iso = datetime.strptime(departure, '%d/%m/%Y').date().isoformat()
            except ValueError:
                # Si el formato de fecha es incorrecto, no lo incluimos
                pass
        # ----------------------------------------------------------------------
        
        # Si el valor no se puede determinar (es None), usamos 0 centavos como fallback.
        total_payout_cents = total_in_cents if total_in_cents is not None else 0
        guest_paid_cents = total_in_cents if total_in_cents is not None else 0
        taxes_cents = tax_in_cents if tax_in_cents is not None else 0

        # Prepare payload for HostHub
        payload = {
            "type": "Booking",
            "date_from": date_from_iso,  # <-- AÑADIDO: Fecha de llegada
            "date_to": date_to_iso,      # <-- AÑADIDO: Fecha de salida
            "taxes": {
                'cents': taxes_cents,
                'currency': 'EUR'
            },
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
                    "tax_cents": tax_in_cents,
                    "total_cents": total_in_cents
                }
            })
        }
        
        # Limpiamos el payload de fechas si el parseo falló (valor es None)
        if date_from_iso is None:
            payload.pop('date_from', None)
        if date_to_iso is None:
            payload.pop('date_to', None)

        url = f"{self.base_url}/calendar-events/{calendar_event_id}"
        response = requests.post(url, headers=self.headers, data=json.dumps(payload))

        if response.status_code in (200, 201):
            return response.json()
        else:
            # Incluye el payload en el error para una futura depuración
            raise Exception(f"Error updating booking: {response.status_code} - {response.text} - payload: {json.dumps(payload)}")

hosthub = HostHubAPI()
