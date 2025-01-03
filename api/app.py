from flask import Flask
from .contact import blueprint as contact_blueprint

app = Flask(__name__)

# Register the home blueprint
app.register_blueprint(contact_blueprint, url_prefix='/')

if __name__ == "__main__":
    app.run(debug=True)