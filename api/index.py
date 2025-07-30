from flask import Flask, request, redirect
import os
import resend

app = Flask(__name__)
resend.api_key = os.environ["RESEND_API_KEY"]

@app.route("/contact", methods=["POST"])
def contact():
    name = request.form.get("name")
    email = request.form.get("email")
    comment = request.form.get("comment")

    params = {
        "from": os.environ.get("RESEND_DEMO_SENDER_EMAIL"),  # Usa tu remitente verificado
        "to": [os.environ.get("YOUR_EMAIL_1"), os.environ.get("YOUR_EMAIL_2")],
        "subject": f"Nuevo mensaje de contacto de {name}",
        "html": f"""
            <p>Hola,</p>
            <p>Has recibido un nuevo mensaje de contacto:</p>
            <ul>
                <li><strong>Nombre:</strong> {name}</li>
                <li><strong>Email:</strong> {email}</li>
                <li><strong>Mensaje:</strong> {comment}</li>
            </ul>
            <p>¡Saludos!</p>
        """,
    }

    email_response = resend.Emails.send(params)
    print(email_response)
    return redirect("/success")

if __name__ == "__main__":
    app.run(debug=True)