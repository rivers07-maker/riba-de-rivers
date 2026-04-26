import time
import logging
from datetime import datetime, timedelta
from flask import Blueprint, jsonify
from .vendor_services.hosthub import hosthub

blueprint = Blueprint("availability", __name__)

# In-memory cache for availability data
_availability_cache = {
    "data": None,
    "expiry": 0
}
CACHE_DURATION = 900  # 15 minutes


def _expand_date_range(date_from_str, date_to_str):
    """
    Expands a date range into individual date strings (YYYY-MM-DD).
    Excludes date_to since that is the checkout day (available for new bookings).
    """
    dates = []
    try:
        date_from = datetime.strptime(date_from_str, "%Y-%m-%d").date()
        date_to = datetime.strptime(date_to_str, "%Y-%m-%d").date()
        current = date_from
        while current < date_to:  # Exclude date_to (checkout day)
            dates.append(current.isoformat())
            current += timedelta(days=1)
    except (ValueError, TypeError) as e:
        logging.warning(f"Error expanding date range {date_from_str} to {date_to_str}: {e}")
    return dates


def get_cached_availability():
    """
    Returns a list of unavailable date strings (YYYY-MM-DD) from Hosthub,
    with 15-minute in-memory caching.
    """
    current_time = time.time()
    if _availability_cache["data"] is not None and current_time < _availability_cache["expiry"]:
        return _availability_cache["data"]

    try:
        logging.info("Fetching fresh availability from Hosthub...")
        today = datetime.now().date()
        date_from = today.isoformat()
        date_to = (today + timedelta(days=365)).isoformat()

        events = hosthub.get_calendar_events(date_from, date_to)

        unavailable_dates = set()
        for event in events:
            event_type = event.get("type", "")
            # Both "Booking" and "Hold" (block) types make dates unavailable
            if event_type in ("Booking", "Hold"):
                ef = event.get("date_from", "")
                et = event.get("date_to", "")
                if ef and et:
                    unavailable_dates.update(_expand_date_range(ef, et))

        result = sorted(list(unavailable_dates))
        _availability_cache["data"] = result
        _availability_cache["expiry"] = current_time + CACHE_DURATION
        logging.info(f"Fetched {len(result)} unavailable dates from Hosthub.")
        return result

    except Exception as e:
        logging.error(f"Failed to fetch availability: {e}")
        # Return old data if available, even if expired
        if _availability_cache["data"] is not None:
            return _availability_cache["data"]
        raise


@blueprint.route('/api/availability', methods=['GET'])
def get_availability():
    """
    Returns a JSON object with an array of unavailable dates (YYYY-MM-DD).
    Used by the frontend Flatpickr calendar to disable booked/blocked dates.
    """
    try:
        unavailable_dates = get_cached_availability()
        return jsonify({"unavailable_dates": unavailable_dates})
    except Exception as e:
        logging.error(f"Error in availability endpoint: {e}")
        return jsonify({"error": str(e), "unavailable_dates": []}), 500
