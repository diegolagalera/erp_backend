import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email.mime.text import MIMEText

from email import encoders

def send_email(sender_email, sender_password, receiver_email, subject, body, attachment_path):
    # Configurar el servidor SMTP
    smtp_server = "smtp.gmail.com"  # Cambia esto si usas otro proveedor de correo
    port = 587  # El puerto para TLS

    # Crear el objeto mensaje
    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = receiver_email
    msg['Subject'] = subject

    # Agregar el cuerpo del correo
    msg.attach(MIMEText(body, 'plain'))

    # Adjuntar el PDF al correo
    with open(attachment_path, "rb") as attachment:
        part = MIMEBase('application', 'octet-stream')
        part.set_payload(attachment.read())
    encoders.encode_base64(part)
    part.add_header('Content-Disposition', f"attachment; filename= {attachment_path}")
    msg.attach(part)

    # Iniciar una conexión segura con el servidor y enviar el correo
    try:
        server = smtplib.SMTP(smtp_server, port)
        server.starttls()
        server.login(sender_email, sender_password)
        server.sendmail(sender_email, receiver_email, msg.as_string())
        print("Correo enviado exitosamente")
    except Exception as e:
        print(f"Error al enviar el correo: {e}")
    finally:
        server.quit()