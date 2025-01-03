from flask import Flask
from home import app as home_blueprint

app = Flask(__name__)

# Register the home blueprint
app.register_blueprint(home_blueprint, url_prefix='/')

if __name__ == "__main__":
    app.run(debug=True)