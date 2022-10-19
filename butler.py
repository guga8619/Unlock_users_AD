#! /user/bin/env python3

from reademail import readEmail
from seg import checkunlock
from ldap_connect import unlockuser
from sendemail import sendEmail
import time

def timer():
    data_email=readEmail()
    if data_email == "No hay correos para desbloquear":
        time.sleep(3)
    else:
        for mail in data_email:
            if checkunlock(mail["user"],mail["email"]) != "El usuario ya fue desbloqueado 2 veces de manera automatica, por favor comunicarse con mesa de ayuda de sistemas para un nuevo desbloqueo":
                unlock=unlockuser(mail["user"])
                mail["result"]=unlock
                sendEmail(mail)
            else:
                mail["result"]=checkunlock(mail["user"],mail["email"])
                sendEmail(mail)
        time.sleep(3)

if __name__=="__main__":
    while True:
        timer()
    