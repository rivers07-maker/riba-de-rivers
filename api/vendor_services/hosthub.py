import requests
import os
import json
import logging
from datetime import datetime
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
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
        self.session = self._setup_session()

    def _setup_session(self):
        session = requests.Session()
        retry_strategy = Retry(
            total=5,
            backoff_factor=1,
            status_forcelist=[429, 502, 503, 504],
            allowed_methods=["GET", "POST"]
        )
        adapter = HTTPAdapter(max_retries=retry_strategy)
        session.mount("https://", adapter)
        session.mount("http://", adapter)
        session.headers.update(self.headers)
        return session

    def create_booking(self, date_from= "<date>", date_to= "<date>", metadata={}):
        url = f"{self.base_url}/rentals/{HOSTHUB_RENTAL_ID}/calendar-events"
        payload = {
            "type": "Booking",
            "date_from": date_from,
            "date_to": date_to,
            **metadata
        }
        
        response = self.session.post(url, data=json.dumps(payload))

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
        total_details = data.get('amount_details') or {}
        tax_in_cents = data.get('amount_tax') or total_details.get('amount_tax') or 0

        # Prepare payload for HostHub.
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
        response = self.session.post(url, data=json.dumps(payload))

        if response.status_code in (200, 201):
            return response.json()
        else:
            raise Exception(f"Error updating booking: {response.status_code} - {response.text} - payload: {json.dumps(payload)}")

    def get_rental_settings(self):
        """
        Fetches the current rates and settings for the rental.
        Currently focuses on extracting nightly rates and extra person fees.
        """
        try:
            # 1. Get Rate Plans for the rental
            rate_plans_url = f"{self.base_url}/rentals/{HOSTHUB_RENTAL_ID}/rate-plans"
            response = self.session.get(rate_plans_url)
            response.raise_for_status()
            rate_plans = response.json().get('data', [])
            
            # Find the default rate plan
            default_plan = next((p for p in rate_plans if p.get('default')), None)
            if not default_plan and rate_plans:
                default_plan = rate_plans[0]
            
            if not default_plan:
                raise Exception("No rate plans found for rental.")

            # 2. Get Daily Rates for the default plan
            rates_url = f"{self.base_url}/rate-plans/{default_plan['id']}/rates"
            response = self.session.get(rates_url)
            response.raise_for_status()
            daily_rates = response.json().get('data', [])

            if not daily_rates:
                raise Exception("No daily rates found.")

            # Get today's rate (or the first available)
            today_str = datetime.now().strftime("%Y-%m-%d")
            today_rate = next((r for r in daily_rates if r['date'] == today_str), daily_rates[0])

            # Extract settings
            settings = {
                "nightly_rate": today_rate.get('amount', {}).get('cents', 0) / 100.0,
                "extra_person_fee": today_rate.get('extra_cost_per_person', {}).get('cents', 0) / 100.0,
                "extra_person_threshold": today_rate.get('amount_of_people_threshold', 2),
                "currency": today_rate.get('amount', {}).get('currency', 'EUR'),
                # Updated fallbacks as per user screenshot
                "cleaning_fee": 25.0,
                "pet_fee": 10.0,
            }

            # 3. Dynamic Fee Discovery (Optional/Advanced)
            # We'll stick to the standard fallbacks for now to match the user's main dashboard configuration
            # as the proxy logic might pick up short-stay variations (like 20€) which can be confusing.
            
            return settings
        except Exception as e:
            logging.error(f"Error fetching Hosthub settings: {e}")
            raise

hosthub = HostHubAPI()
