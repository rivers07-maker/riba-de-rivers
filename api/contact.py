from flask import request, redirect, render_template, Blueprint
from supabase import create_client, Client
from dotenv import load_dotenv
import os
import logging
import resend

blueprint = Blueprint("contact", __name__, template_folder='../public')

load_dotenv()

# Configure logging
logging.basicConfig(level=logging.DEBUG)

# Supabase credentials
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

# Resend credentials (nuevas)
RESEND_API_KEY = os.getenv("RESEND_API_KEY")
YOUR_EMAIL_1 = os.getenv("YOUR_EMAIL_FOR_NOTIFICATIONS")
YOUR_EMAIL_2 = os.getenv("YOUR_EMAIL_2")
RESEND_DEMO_SENDER_EMAIL = os.getenv("RESEND_DEMO_SENDER_EMAIL") # Usamos el correo de demostración

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

            # Insertar en Supabase (código existente)
            supabase.table('contact_submissions').insert(new_submission).execute()
            logging.info("Submission successfully inserted into Supabase.")

            # Lógica para enviar el email de notificación con Resend
            if RESEND_API_KEY and YOUR_EMAIL_1 and YOUR_EMAIL_2 and RESEND_DEMO_SENDER_EMAIL:
                try:
                    resend.api_key = RESEND_API_KEY  # Configura la API key

                    subject = f"Nuevo mensaje de contacto de {new_submission['name']}"
                    html_content = f"""
                        <p>Hola,</p>
                        <p>Has recibido un nuevo mensaje de contacto:</p>
                        <ul>
                        <li><strong>Nombre:</strong> {new_submission['name']}</li>
                        <li><strong>Email:</strong> {new_submission['email']}</li>
                        <li><strong>Mensaje:</strong> {new_submission['comment']}</li>
                        </ul>
                        <p>¡Saludos!</p>
                    """

                    response = resend.Emails.send({
                        "from": RESEND_DEMO_SENDER_EMAIL,
                        "to": [YOUR_EMAIL_1, YOUR_EMAIL_2],
                        "subject": subject,
                        "html": html_content,
                    })

                    if response.get('id'):
                        logging.info(f"Email de notificación enviado con éxito. ID: {response.get('id')}")
                    else:
                        logging.error(f"Error al enviar email de notificación: {response}")

                except Exception as email_e:
                    logging.error(f"Excepción al intentar enviar email con Resend: {email_e}")
            else:
                logging.warning("No se pudo enviar el email de notificación. Verifique la configuración de Resend o las variables de entorno.")

            return redirect('/success')
        except Exception as e:
            logging.error(f"Error al manejar la solicitud POST o al insertar en Supabase: {e}")
            return "Internal Server Error", 500
    else:
        try:
            submissions = list(supabase.table('contact_submissions').select().execute())
            logging.debug(f"Submissions: {submissions}")

            return render_template("contact.html", submissions=submissions)

        except Exception as e:
            logging.error(f"Error al manejar la solicitud GET: {e}")
            return "Internal Server Error", 500
