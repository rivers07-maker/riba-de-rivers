from flask import request, redirect, render_template, Blueprint
from dotenv import load_dotenv
import os
import logging

blueprint = Blueprint("booking", __name__, template_folder='../public')

load_dotenv()

# Configure logging
logging.basicConfig(level=logging.DEBUG)


@blueprint.route("/booking", methods=["GET", "POST"])
def booking():
    if request.method == "POST":
        try:
            new_booking = {
                'name': request.form.get('name'),
                'email': request.form.get('email'),
                'comment': request.form.get('comment')
            }

            logging.debug(f"New booking: {new_booking}")

            supabase.table('submissions').insert(new_submission).execute()

            return redirect('/success')
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
