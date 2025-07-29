import sys
import os
from .app import app

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Import the Flask app instance from app.py
try:
    if __name__ == "__main__":
        app.run(debug=True)
except Exception as e:
    print(f"Error importing app: {e}")
    raise

# Expose the WSGI application object
application = app
