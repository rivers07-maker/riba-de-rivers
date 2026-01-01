import time
import logging
from flask import Blueprint, jsonify, request
from .vendor_services.hosthub import hosthub

blueprint = Blueprint("rates", __name__)

# Simple in-memory cache
_cache = {
    "data": None,
    "expiry": 0
}
CACHE_DURATION = 3600  # 1 hour

def get_cached_rates():
    current_time = time.time()
    if _cache["data"] and current_time < _cache["expiry"]:
        return _cache["data"]

    try:
        logging.info("Fetching fresh rates from Hosthub...")
        settings = hosthub.get_rental_settings()
        _cache["data"] = settings
        _cache["expiry"] = current_time + CACHE_DURATION
        return settings
    except Exception as e:
        logging.error(f"Failed to fetch rates: {e}")
        # Return old data if available, even if expired, as a fallback
        if _cache["data"]:
            return _cache["data"]
        raise

@blueprint.route('/api/rates', methods=['GET'])
def get_rates():
    try:
        force_refresh = request.args.get('force_refresh', 'false').lower() == 'true'
        if force_refresh:
            global _cache
            _cache = {"data": None, "expiry": 0}
            logging.info("Forcing rate cache refresh...")
        
        rates = get_cached_rates()
        return jsonify(rates)
    except Exception as e:
        return jsonify({"error": str(e)}), 500
