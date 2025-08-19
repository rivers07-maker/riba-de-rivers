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
BUSINESS_EMAIL_1 = os.getenv("BUSINESS_EMAIL_1")
BUSINESS_EMAIL_2 = os.getenv("BUSINESS_EMAIL_2")
RESEND_DEMO_SENDER_EMAIL = os.getenv("RESEND_DEMO_SENDER_EMAIL") # Usamos el correo de demostración

try:
    supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)
except Exception as e:
    logging.error(f"Error creating Supabase client: {e}")
    raise


def send_notification_email(new_submission):
    """
    Envía un email de notificación usando Resend con los datos de la nueva solicitud de contacto.
    """
    if RESEND_API_KEY and BUSINESS_EMAIL_1 and BUSINESS_EMAIL_2 and RESEND_DEMO_SENDER_EMAIL:
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
            """

            response = resend.Emails.send({
                "from": RESEND_DEMO_SENDER_EMAIL,
                "to": [BUSINESS_EMAIL_1, BUSINESS_EMAIL_2],
                "subject": subject,
                "html": html_content,
            })

        except Exception as e:
           logging.error(f"Error sending email: {e}")
           if hasattr(e, 'response'):
               logging.error(f"Resend response: {getattr(e.response, 'text', 'Unavailable')}")
            raise Exception("Failed to send email", e)   
    else:
        logging.error("No se pudo enviar el email de notificación. Verifique la configuración de Resend o las variables de entorno.")
        raise EnvironmentError('Estan faltando las variables de entorno requeridas para el enviar el email de notificacion')


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

            # Llamar a la función para enviar el email de notificación
            send_notification_email(new_submission)

            return redirect('/success')
        except Exception as e:
            logging.error(f"Error al manejar la solicitud POST o al insertar en Supabase: {e}")
            return "Internal Server Error", 500
    else:
        return render_template("contact.html")