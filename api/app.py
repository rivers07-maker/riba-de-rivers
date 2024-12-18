from flask import Flask, request, url_for, redirect, render_template
from supabase import create_client, Client
from dotenv import load_dotenv
import os

load_dotenv()

app = Flask(__name__)

# Replace these placeholders with your actual Supabase credentials
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

@app.route("/", methods=["GET", "POST"])
def home():
    if request.method == "POST":
        new_submission = {
            'name': request.form.get('name'),
            'phone': request.form.get('phone'),
            'email': request.form.get('email'),
            'guests': int(request.form.get('guests')),
            'arrival': request.form.get('arrival'),
            'departure': request.form.get('departure'),
            'comment': request.form.get('comment')
        }
        
        supabase.table('submissions').insert(new_submission).execute()
        
        return redirect(url_for("success"))
    
    else:
        submissions = list(supabase.table('submissions').select().execute())
        return render_template("contact.html", submissions=submissions)

@app.route("/success")
def success():
    return render_template("success.html")

if __name__ == "__main__":
    app.run(debug=True)
