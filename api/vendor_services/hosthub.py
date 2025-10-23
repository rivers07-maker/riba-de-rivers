from dotenv import load_dotenv
import requests
import os
import json
from ..utils import load_configuration

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
    
    def create_temporary_booking(self, type="Hold", date_from= "<date>", date_to= "<date>"):
        url = f"{self.base_url}/rentals/{HOSTHUB_RENTAL_ID}/calendar-events"
        response = requests.post(url, headers=self.headers, data=json.dumps({
            "type": type,
            "date_from": date_from,
            "date_to": date_to
        }))
        
        if response.status_code == 200:
            return response.json()
        else:
            raise Exception(f"Error creating temporary booking: {response.text}")


    def update_booking(self, calendar_event_id, payment_data):
        """
        Update a HostHub calendar event with booking/payment details mapped from
        Stripe Checkout Session or PaymentIntent data.

        Args:
            calendar_event_id (str): HostHub calendar event id to update.
            payment_data (dict): A dict representing either a Stripe Checkout Session
                or a Stripe PaymentIntent (or a wrapper containing one of those under
                the key 'payment_data').

        The function will attempt to extract the following values (with fallbacks):
            - subtotal (amount_subtotal / amount)
            - total (amount_total / amount_received / amount)
            - tax (total_details.amount_tax or amount_tax)
            - metadata fields: cleaning_fee, other_fees, reservation_id, calendar_event_id

        Amounts in Stripe are in the smallest currency unit (cents for EUR). The
        payload sent to HostHub will include amounts converted to euros (float with
        2 decimal places) under a `price_details` object. The raw payment_data is
        stored in `notes` for traceability.
        """

        # Normalize wrapper (sometimes callers pass {'payment_data': {...}})
        data = payment_data
        if isinstance(payment_data, dict) and 'payment_data' in payment_data and isinstance(payment_data['payment_data'], dict):
            data = payment_data['payment_data']

        # Helper: parse amounts from metadata or fields and normalize to cents (int)
        def parse_amount_raw(val):
            """Try to parse a metadata value into integer cents.
            Accepts: int (assumed cents), numeric strings like '115.00' (euros),
            integer-like strings ('11500' assumed cents unless small), and floats.
            Heuristic: if numeric value < 1000 treat as euros and multiply by 100.
            """
            if val is None:
                return None
            # Integers already (assume cents)
            if isinstance(val, int):
                return val
            try:
                s = str(val).strip()
                # Pure digits: ambiguous between cents and euros. Use heuristic.
                if s.isdigit():
                    v = int(s)
                    # If a small number (<1000) it's likely euros (e.g. '115'),
                    # so convert to cents. If large it's probably already cents.
                    return v * 100 if v < 1000 else v
                # Otherwise parse as float (e.g. '115.00')
                f = float(s)
                # If the float looks like an integer number of euros, convert to cents
                return int(round(f * 100))
            except Exception:
                return None

        def cents_to_eur_float(cents):
            return round(cents / 100.0, 2) if cents is not None else None

        # Extract common amount fields (all in cents)
        subtotal = None
        total = None
        tax = None

        # Checkout Session fields
        if isinstance(data, dict):
            subtotal = data.get('amount_subtotal') or data.get('amount') or data.get('amount_received')
            total = data.get('amount_total') or data.get('amount') or data.get('amount_received')

            # total_details may include tax breakdown
            td = data.get('total_details') or {}
            tax = td.get('amount_tax') or data.get('amount_tax')

        # If any of those are strings or floats, try to coerce via parse_amount_raw
        subtotal = parse_amount_raw(subtotal) if subtotal is not None else None
        total = parse_amount_raw(total) if total is not None else None
        tax = parse_amount_raw(tax) if tax is not None else None

        # Metadata-based breakdown: prefer explicit metadata values if present
        metadata = (data.get('metadata') or {}) if isinstance(data, dict) else {}

        cleaning_meta_keys = ['cleaning_fee', 'cleaning', 'cleaning_amount']
        other_meta_keys = ['other_fees', 'other_fee', 'extra_fees', 'extras']

        def find_meta_amount(keys):
            for k in keys:
                if k in metadata and metadata[k] not in (None, ''):
                    a = parse_amount_raw(metadata[k])
                    if a is not None:
                        return a
            return None

        # Prefer explicit metadata fields if provided (booking_value, cleaning_fee, other_fees)
        booking_value_meta = None
        for key in ['booking_value', 'booking_value_cents', 'bookingAmount']:
            if key in metadata and metadata[key] not in (None, ''):
                booking_value_meta = parse_amount_raw(metadata[key])
                break

        cleaning_fee = find_meta_amount(cleaning_meta_keys)
        other_fees = find_meta_amount(other_meta_keys)

        # If explicit booking_value metadata is present, prefer it
        booking_value = booking_value_meta if booking_value_meta is not None else None

        # If we don't have an explicit booking value, try to derive it from subtotal
        if booking_value is None and subtotal is not None:
            # subtotal is typically the amount before tax/shipping/discounts
            booking_value = subtotal
            if cleaning_fee:
                booking_value = booking_value - cleaning_fee
            if other_fees:
                booking_value = booking_value - other_fees

        # If booking_value ended up None but total exists, use total as fallback
        if booking_value is None and total is not None:
            booking_value = total

        # Prepare payload for HostHub. HostHub API schema isn't included here,
        # so send a clear `price_details` object plus some external references.
        payload = {
            "type": "Booking",
            "price_details": {
                "booking_value": cents_to_eur_float(booking_value),
                "cleaning_fee": cents_to_eur_float(cleaning_fee),
                "other_fees": cents_to_eur_float(other_fees),
                "taxes": cents_to_eur_float(tax),
                "total_value": cents_to_eur_float(total),
                "currency": (data.get('currency') if isinstance(data, dict) else None) or "eur"
            },
            "external_references": {
                "hosthub_calendar_event_id": calendar_event_id,
                "reservation_id": metadata.get('reservation_id') if metadata.get('reservation_id') not in (None, '') else None,
                # Try to include both session id and payment intent id when available
                "stripe_session_id": data.get('id') if data.get('object') == 'checkout.session' else None,
                "stripe_payment_intent": data.get('payment_intent') if data.get('object') == 'checkout.session' else (data.get('id') if data.get('object') == 'payment_intent' else None)
            },
            "notes": json.dumps({
                "raw_payment_data": data,
                "derived": {
                    "booking_value_cents": booking_value,
                    "booking_value_meta_cents": booking_value_meta,
                    "cleaning_fee_cents": cleaning_fee,
                    "other_fees_cents": other_fees,
                    "tax_cents": tax,
                    "total_cents": total
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