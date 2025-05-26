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

    