from flask import Flask
from .contact import blueprint as contact_blueprint
# from .booking import blueprint as booking_blueprint

app = Flask(__name__)

# Register the contact blueprint
app.register_blueprint(contact_blueprint, url_prefix='/')

# Register the booking blueprint
# app.register_blueprint(booking_blueprint, url_prefix='/')