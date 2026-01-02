import requests
import os
import json
import logging
from datetime import datetime
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
from ..utils import load_configuration, parse_date

# Configure logger
logger = logging.getLogger(__name__)

# Load environment variables
load_configuration()

HOSTHUB_KEY = os.getenv("HOSTHUB_KEY")
HOSTHUB_RENTAL_ID = os.getenv("HOSTHUB_RENTAL_ID")


class HostHubAPI:
    def __init__(self):
        self.base_url = "https://app.hosthub.com/api/2019-03-01"
        self.headers = {
            "Authorization": f"{HOSTHUB_KEY}",
            "Content-Type": "application/json",
        }
        self.session = self._setup_session()

    def _setup_session(self):
        session = requests.Session()
        retry_strategy = Retry(
            total=5,
            backoff_factor=1,
            status_forcelist=[429, 502, 503, 504],
            allowed_methods=["GET", "POST"],
        )
        adapter = HTTPAdapter(max_retries=retry_strategy)
        session.mount("https://", adapter)
        session.mount("http://", adapter)
        session.headers.update(self.headers)
        return session

    def create_booking(self, date_from="<date>", date_to="<date>", metadata={}):
        url = f"{self.base_url}/rentals/{HOSTHUB_RENTAL_ID}/calendar-events"
        payload = {
            "type": "Booking",
            "date_from": date_from,
            "date_to": date_to,
            **metadata,
        }

        response = self.session.post(url, data=json.dumps(payload))

        if response.status_code == 200:
            logger.info("Booking created successfully.")
            return response.json()
        else:
            raise Exception(f"Error creating temporary booking: {response.text}")

    def update_booking(self, calendar_event_id, payment_data):
        # Normalize wrapper (sometimes callers pass {'payment_data': {...}})
        data = payment_data
        if (
            isinstance(payment_data, dict)
            and "payment_data" in payment_data
            and isinstance(payment_data["payment_data"], dict)
        ):
            data = payment_data["payment_data"]

        total_in_cents = data.get("amount") or data.get("amount_received")
        try:
            total_payout_cents = (
                int(total_in_cents) if total_in_cents is not None else 0
            )
            guest_paid_cents = int(total_in_cents) if total_in_cents is not None else 0
        except (ValueError, TypeError) as e:
            logger.warning(
                f"Error converting amount to int: {total_in_cents}. Defaulting to 0. Error: {e}"
            )
            total_payout_cents = 0
            guest_paid_cents = 0

        # Extract metadata
        metadata = data.get("metadata", {})
        arrival = metadata.get("arrival_date")
        departure = metadata.get("departure_date")
        date_from_iso = parse_date(arrival)
        date_to_iso = parse_date(departure)

        if not date_from_iso or not date_to_iso:
            logger.warning(
                f"MISSING DATES for Event ID {calendar_event_id}. Parsed: {date_from_iso} / {date_to_iso}"
            )

        notes_data = {
            "payment_intent_id": data.get("id"),
            "total_cents": total_in_cents,
            "raw_payment_data": data,
        }
        notes_str = HostHubAPI.format_payment_notes(notes_data)

        # Build payload ensuring guest details are preserved/set
        payload = {
            "type": "Booking",
            "total_payout": {"cents": total_payout_cents, "currency": "EUR"},
            "guest_paid": {"cents": guest_paid_cents, "currency": "EUR"},
            "notes": notes_str,
            # Pass guest details to ensure they are set/updated correctly
            "guest_name": metadata.get("guest_name"),
            "guest_email": metadata.get("guest_email"),
            "guest_phone": metadata.get("guest_phone"),
            "guest_adults": metadata.get("guest_adults"),
            "guest_children": metadata.get("guest_children"),
        }
        if date_from_iso:
            payload["date_from"] = date_from_iso
        if date_to_iso:
            payload["date_to"] = date_to_iso

        url = f"{self.base_url}/calendar-events/{calendar_event_id}"
        logger.info(
            f"Updating booking {calendar_event_id} with data: {json.dumps(payload)}"
        )

        try:
            response = requests.post(
                url, headers=self.headers, data=json.dumps(payload)
            )
            if response.status_code in (200, 201):
                logger.info(f"Successfully updated booking {calendar_event_id}")
                return response.json()
            else:
                is_html_error = (
                    response.status_code >= 500 and "<html" in response.text.lower()
                )
                error_preview = (
                    "Server Error (HTML Content)" if is_html_error else response.text
                )
                logger.error(
                    f"HostHub API Error {response.status_code}: {error_preview}"
                )
                raise Exception(
                    f"Error updating booking: {response.status_code} - {error_preview}"
                )
        except requests.RequestException as e:
            logger.critical(f"Network error connecting to HostHub: {e}")
            raise

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
            rate_plans = response.json().get("data", [])

            # Find the default rate plan
            default_plan = next((p for p in rate_plans if p.get("default")), None)
            if not default_plan and rate_plans:
                default_plan = rate_plans[0]

            if not default_plan:
                raise Exception("No rate plans found for rental.")

            # 2. Get Daily Rates for the default plan
            rates_url = f"{self.base_url}/rate-plans/{default_plan['id']}/rates"
            response = self.session.get(rates_url)
            response.raise_for_status()
            daily_rates = response.json().get("data", [])

            if not daily_rates:
                raise Exception("No daily rates found.")

            # Get today's rate (or the first available)
            today_str = datetime.now().strftime("%Y-%m-%d")
            today_rate = next(
                (r for r in daily_rates if r["date"] == today_str), daily_rates[0]
            )

            # Extract settings
            settings = {
                "nightly_rate": today_rate.get("amount", {}).get("cents", 0) / 100.0,
                "extra_person_fee": today_rate.get("extra_cost_per_person", {}).get(
                    "cents", 0
                )
                / 100.0,
                "extra_person_threshold": today_rate.get(
                    "amount_of_people_threshold", 2
                ),
                "currency": today_rate.get("amount", {}).get("currency", "EUR"),
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

    @staticmethod
    def format_payment_notes(data):
        """
        Formats the payment data for the Hosthub UI.
        Receives a dict with key fields and returns a presentable string.
        """
        try:
            # Allows for both flat dict and nested dict (raw/derived)
            raw = data.get("raw_payment_data", data)
            derived = data.get("derived", data)

            # Payment ID extraction
            payment_id = derived.get("payment_intent_id") or raw.get("id") or "-"

            # Amount calculation
            # Robustly handle 0 as a valid amount
            total_cents = derived.get("total_cents")
            if total_cents is None:
                total_cents = raw.get("amount")

            if total_cents is not None:
                try:
                    total_eur = f"€{int(total_cents) / 100:.2f}"
                except (ValueError, TypeError):
                    total_eur = "-"
            else:
                total_eur = "-"

            # Status determination
            succeeded = raw.get("status") == "succeeded"
            status = "Successful" if succeeded else "Failed"

            # Method determination
            method = raw.get("payment_method_types", ["-"])
            if isinstance(method, list) and method:
                method_str = method[0].capitalize()
            elif isinstance(method, str):
                method_str = method.capitalize()
            else:
                method_str = "-"

            # Date determination and formatting
            date_ts = raw.get("created")
            if date_ts:
                try:
                    # Using utcfromtimestamp
                    date_str = datetime.utcfromtimestamp(int(date_ts)).strftime(
                        "%d/%m/%Y"
                    )
                except Exception:
                    date_str = str(date_ts)
            else:
                date_str = "-"

            # Returning the formatted string (using | for Hosthub compatibility)
            return f"Stripe Payment | Payment ID: {payment_id} | Amount: {total_eur} | Status: {status} | Method: {method_str} | Date: {date_str}"
        except Exception as e:
            logger.error(f"Error formating payment notes: {e}")
            return "Error formatting payment notes"


hosthub = HostHubAPI()
