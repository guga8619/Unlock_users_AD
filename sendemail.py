from email.message import EmailMessage
import smtplib
import os
from dotenv import load_dotenv

SERVEREMAIL=os.getenv("SERVEREMAIL")
USEREMAIL=os.getenv("USEREMAIL")
PASSWORDEMAIL=os.getenv("PASSWORDEMAIL")

load_dotenv()
def sendEmail(data):
	try:
		message = EmailMessage()
		email_subject = "Respuesta automatica, no contestar"
		sender_email_address = USEREMAIL
		receiver_email_address = data["email"]
		message['Subject'] = email_subject 
		message['From'] = sender_email_address 
		message['To'] = receiver_email_address
		msg = f'Estado del usuario: {data["user"]}\n{data["result"]}\n\nGracias por utilizar el servicio de desbloqueo automatico creado por Gustavo Armani'
		message.set_content(msg)
		username = USEREMAIL
		password = PASSWORDEMAIL
		server = smtplib.SMTP(f'{SERVEREMAIL}:587')
		server.starttls()
		server.login(username,password)
		server.send_message(message)
		server.quit()
		return True
	except:
		return False