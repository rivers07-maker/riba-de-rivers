from flask import Flask, render_template, request, redirect, url_for
import os
from supabase import create_client, Client

app = Flask(__name__)

# Replace these placeholders with your actual Supabase credentials
SUPABASE_URL = os.getenv("https://pmfqmcguoviqxupksjlv.supabase.co")
SUPABASE_KEY = os.getenv("eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InBtZnFtY2d1b3ZpcXh1cGtzamx2Iiwicm9sZSI6ImFub24iLCJpYXQiOjE3MzM5MzIwNTksImV4cCI6MjA0OTUwODA1OX0.7bj1X1PgE5OZJq-PkuYLgm5lyLkCpN5Eronl7zyO7kk")

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
    return "<h1>Form submitted successfully!</h1>Y1:0"

if __name__ == "__main__":
    app.run(debug=True)
