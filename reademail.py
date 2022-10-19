import imaplib
import email
import os
from dotenv import load_dotenv

SERVEREMAIL=os.getenv("SERVEREMAIL")
USEREMAIL=os.getenv("USEREMAIL")
PASSWORDEMAIL=os.getenv("PASSWORDEMAIL")

load_dotenv()
def readEmail():
    #Conexion al servidor
    server= imaplib.IMAP4_SSL(SERVEREMAIL)
    server.login(USEREMAIL,PASSWORDEMAIL)
    server.select("inbox")
    #Buscar  correos por asunto Desbloquear
    tmp, email_data = server.search(None, '(SUBJECT "Desbloquear")')
    if len(email_data[0].split())==0:
        result="No hay correos para desbloquear"
        return result
    else:
        emails=[]
        for num in email_data[0].split():
            #Recuperando correos
            tmp, data = server.fetch(num, '(RFC822)')
            content=data[0][1].decode("utf-8")
            email_message = email.message_from_string(content)
            email_message_from=email_message['From']
            email_message_user_unlock=str(email_message['Subject']).split(" ")[-1]
            email_message_user_email=email_message_from[int(email_message_from.find("<"))+1:int(email_message_from.find(">"))]
            email_message_data={"email":email_message_user_email,"user":email_message_user_unlock}
            emails.append(email_message_data)
            server.store((num) , '+FLAGS', '\\Deleted')
        server.expunge()
        return emails

if __name__ =="__main__":
    print(readEmail())