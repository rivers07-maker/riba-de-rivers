import os
from dotenv import load_dotenv, find_dotenv

def load_configuration():
    # Buscar el archivo .env correcto basado en la variable ENV
    env_file = find_dotenv(f'.env.{os.getenv("ENV", "development")}')
    
    # Cargar las variables de entorno
    load_dotenv(env_file)
    