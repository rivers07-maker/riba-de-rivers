import os
from dotenv import load_dotenv, find_dotenv

def load_configuration():
    # Cargar .env.ENV si ENV está definido, si no, cargar .env por defecto
    env_name = os.getenv("ENV")
    if env_name:
        env_file = find_dotenv(f'.env.{env_name}')
        load_dotenv(env_file)
    else:
        load_dotenv()  # Carga el archivo .env común
        
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

def find_meta_amount(metadata, keys):
    """Find the first present and valid amount in metadata for the given keys."""
    for k in keys:
        if k in metadata and metadata[k] not in (None, ''):
            a = parse_amount_raw(metadata[k])
            if a is not None:
                return a
    return None


    