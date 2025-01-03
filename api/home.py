from flask import request, url_for, redirect, render_template, Blueprint
from supabase import create_client, Client
from dotenv import load_dotenv
import os
import logging

app = Blueprint("home", __name__, template_folder='../public')

load_dotenv()

# Configure logging
logging.basicConfig(level=logging.DEBUG)

# Replace these placeholders with your actual Supabase credentials
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

# Log the Supabase URL and Key (be careful with logging sensitive information)
logging.debug(f"SUPABASE_URL: {SUPABASE_URL}")
logging.debug(f"SUPABASE_KEY: {SUPABASE_KEY}")

try:
    supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)
except Exception as e:
    logging.error(f"Error creating Supabase client: {e}")
    raise

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/contact", methods=["GET", "POST"])
def contact():
    if request.method == "POST":
        try:
            new_submission = {
                'name': request.form.get('name'),
                'phone': request.form.get('phone'),
                'email': request.form.get('email'),
                'guests': int(request.form.get('guests')),
                'arrival': request.form.get('arrival'),
                'departure': request.form.get('departure'),
                'comment': request.form.get('comment')
            }

            logging.debug(f"New submission: {new_submission}")

            supabase.table('submissions').insert(new_submission).execute()

            return redirect(url_for("home.success"))
        except Exception as e:
            logging.error(f"Error handling POST request: {e}")
            return "Internal Server Error", 500
    else:
        try:
            submissions = list(supabase.table('submissions').select().execute())
            logging.debug(f"Submissions: {submissions}")

            return render_template("contact.html", submissions=submissions)

        except Exception as e:
            logging.error(f"Error handling GET request: {e}")
            return "Internal Server Error", 500

@app.route("/success")
def success():
    return render_template("success.html")