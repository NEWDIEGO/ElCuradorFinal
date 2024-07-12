import smtplib

# Asegurarse de que Python use UTF-8
#sys.setdefaultencoding('utf-8')

# Configuración del servidor SMTP
smtp_server = 'smtp.gmail.com'
smtp_port = 587
smtp_user = 'tu_email@gmail.com'
smtp_password = 'tu_contraseña_de_aplicación'  # Usa la contraseña de aplicación generada

# Dirección de correo del remitente y destinatario (pueden ser iguales para esta prueba)
from_email = 'tu_email@gmail.com'
to_email = 'tu_email@gmail.com'

# Mensaje de correo
subject = "Prueba de conexión SMTP"
body = "Este es un mensaje de prueba para verificar la configuración SMTP."
message = f"Subject: {subject}\n\n{body}"

try:
    # Conectar al servidor SMTP
    server = smtplib.SMTP(smtp_server, smtp_port)
    server.starttls()  # Iniciar la conexión segura
    server.login(smtp_user, smtp_password)  # Iniciar sesión
    server.sendmail(from_email, to_email, message.encode('utf-8'))  # Enviar el correo
    print("Correo enviado exitosamente")
    server.quit()  # Cerrar la conexión
except Exception as e:
    print(f"Error al enviar el correo: {e}")
