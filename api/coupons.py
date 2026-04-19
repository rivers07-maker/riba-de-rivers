from flask import request, Blueprint, jsonify
from supabase import create_client, Client
from dotenv import load_dotenv
import os
import logging
from datetime import date

from .utils import load_configuration

# Initialize Blueprint
blueprint = Blueprint("coupons", __name__)

# Load environment variables
load_configuration()

# Configure logging
logging.basicConfig(level=logging.INFO)

# Supabase credentials
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

try:
    supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)
except Exception as e:
    logging.error(f"Error creating Supabase client for coupons: {e}")
    raise


@blueprint.route("/validate-coupon", methods=["POST"])
def validate_coupon():
    """
    Validates a coupon code against the Supabase 'cupones' table.
    Expects JSON: { "codigo": "VERANO25" }
    Returns JSON: { "valid": true, "descuento": 25 } or { "valid": false, "message": "..." }
    """
    try:
        data = request.get_json()

        if not data or not data.get("codigo"):
            return jsonify({"valid": False, "message": "Código de cupón requerido"}), 400

        codigo = data["codigo"].strip().upper()

        # Query Supabase for the coupon
        response = (
            supabase.table("cupones")
            .select("descuento, activo, expiracion")
            .eq("codigo", codigo)
            .execute()
        )

        # Check if coupon exists and is active
        if response.data and len(response.data) > 0:
            coupon = response.data[0]
            
            # Check expiration date if it exists
            expiration = coupon.get("expiracion")
            if expiration and expiration < date.today().isoformat():
                logging.info(f"Coupon '{codigo}' exists but has expired on {expiration}")
                return jsonify({"valid": False, "message": "Cupón inactivo o expirado"})
                
            if coupon.get("activo"):
                descuento = coupon.get("descuento", 0)
                # Validate discount range
                if 1 <= descuento <= 100:
                    logging.info(f"Coupon '{codigo}' validated successfully: {descuento}% discount")
                    return jsonify({"valid": True, "descuento": descuento})
                else:
                    logging.warning(f"Coupon '{codigo}' has invalid discount value: {descuento}")
                    return jsonify({"valid": False, "message": "Cupón con valor de descuento inválido"})
            else:
                logging.info(f"Coupon '{codigo}' exists but is inactive")
                return jsonify({"valid": False, "message": "Cupón inactivo o expirado"})
        else:
            logging.info(f"Coupon '{codigo}' not found")
            return jsonify({"valid": False, "message": "Cupón no encontrado"})

    except Exception as e:
        logging.error(f"Error validating coupon: {e}")
        return jsonify({"valid": False, "message": "Error al validar el cupón"}), 500
