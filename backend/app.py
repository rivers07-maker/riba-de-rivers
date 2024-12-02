from flask import Flask, render_template, request, redirect, url_for
import sqlite3

app = Flask(__name__)

DATABASE = 'contact.db'

# Home route to display the form
@app.route("/", methods=["GET", "POST"])
def home():
    if request.method == "POST":
        # Capture form data
        name = request.form.get("name")
        phone = request.form.get("phone")
        email = request.form.get("email")
        guests = request.form.get("guests")
        arrival = request.form.get("arrival")
        departure = request.form.get("departure")
        comment = request.form.get("comment")

        # Insert data into SQLite database
        conn = sqlite3.connect(DATABASE)
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO submissions (name, phone, email, guests, arrival, departure, comment)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (name, phone, email, guests, arrival, departure, comment))
        conn.commit()
        conn.close()

        # Redirect or show success message
        return redirect(url_for("success"))

    else:
        return render_template("contact.html")

# Success route
@app.route("/success")
def success():
    return "<h1>Form submitted successfully!</h1>"

# Run the app
if __name__ == "__main__":
    app.run(debug=True)
