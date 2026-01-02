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

def cents_to_eur_float(cents):
    """Converts cents (int) to EUR float value."""
    try:
        return int(cents) / 100.0
    except (ValueError, TypeError):
        return 0.0
        
# Helper para intentar parsear la fecha con múltiples formatos
def parse_date(date_str):
    if not date_str:
        return None
    formats = ['%d/%m/%Y', '%Y-%m-%d', '%Y/%m/%d']
    for fmt in formats:
        try:
            from datetime import datetime
            return datetime.strptime(date_str, fmt).date().isoformat()
        except ValueError:
            continue
    return None