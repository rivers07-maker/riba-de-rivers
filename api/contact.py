from flask import request, redirect, render_template, Blueprint
from supabase import create_client, Client
from dotenv import load_dotenv
import os
import logging

blueprint = Blueprint("contact", __name__, template_folder='../public')

load_dotenv()

# Configure logging
logging.basicConfig(level=logging.DEBUG)

# Replace these placeholders with your actual Supabase credentials
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

try:
    supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)
except Exception as e:
    logging.error(f"Error creating Supabase client: {e}")
    raise

@blueprint.route("/contact", methods=["GET", "POST"])
def contact():
    if request.method == "POST":
        try:
            new_submission = {
                'name': request.form.get('name'),
                'email': request.form.get('email'),
                'comment': request.form.get('comment')
            }

            logging.debug(f"New submission: {new_submission}")

            supabase.table('contact_submissions').insert(new_submission).execute()

            return redirect('/success')
        except Exception as e:
            logging.error(f"Error handling POST request: {e}")
            return "Internal Server Error", 500
    else:
        try:
            submissions = list(supabase.table('contact_submissions').select().execute())
            logging.debug(f"Submissions: {submissions}")

            return render_template("contact.html", submissions=submissions)

        except Exception as e:
            logging.error(f"Error handling GET request: {e}")
            return "Internal Server Error", 500
