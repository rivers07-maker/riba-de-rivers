import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Import the Flask app instance from app.py
try:
    from app import app
except Exception as e:
    print(f"Error importing app: {e}")
    raise

# Expose the WSGI application object
application = app