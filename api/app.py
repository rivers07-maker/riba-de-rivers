from flask import Flask
from .contact import blueprint as contact_blueprint
from .booking import blueprint as booking_blueprint
from .payment_webhooks import blueprint as payment_event_callback_blueprint
from .rates import blueprint as rates_blueprint
from .coupons import blueprint as coupons_blueprint

app = Flask(__name__)

# Register the contact blueprint
app.register_blueprint(blueprint=contact_blueprint, url_prefix="/")

# Register the booking blueprint
app.register_blueprint(blueprint=booking_blueprint, url_prefix="/")

# Register the payment event web-hook listener blueprint
app.register_blueprint(blueprint=payment_event_callback_blueprint, url_prefix="/")

# Register the rates blueprint

app.register_blueprint(blueprint=rates_blueprint, url_prefix="/")

# Register the coupons blueprint
app.register_blueprint(blueprint=coupons_blueprint, url_prefix="/")
