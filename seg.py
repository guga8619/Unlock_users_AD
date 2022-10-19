import os
from datetime import datetime

date=datetime.now().strftime("%d-%m-%Y")
time=datetime.now().strftime("%H:%M")

def createFile():
    with open(f"userslist_{date}.txt","a+") as file:
            file.write(f"Lista de desbloqueos automaticos del {date}\n")

def countUser(user):
    with open(f"userslist_{date}.txt","r+") as file:
        file.seek(0)
        doclines=file.readlines()
        count=0
        for line in doclines:
            if user in line:
                count+=1
        return count

def writeUser(user,email):
    with open(f"userslist_{date}.txt","a+") as file:
        file.write(f"{user} pedido de desbloqueo automatico {date} a las {time}hs ({email})\n")
        return True

def checkunlock(user,email):
    file_exist=os.path.exists(f'userslist_{date}.txt')
    if file_exist:
        try:
            with open(f"userslist_{date}.txt","r+") as file:
                date_document=file.readline().split(" ")[-1].strip()
                if date.strip() == date_document:
                    if countUser(user)<2:
                        write_user_data=writeUser(user,email)
                        return isinstance(write_user_data,bool)       
                    else:
                        result="El usuario ya fue desbloqueado 2 veces de manera automatica, por favor comunicarse con mesa de ayuda de sistemas para un nuevo desbloqueo"
                        return result
        except Exception as e:
            print(e)
    else:
        createFile()
    checkunlock(user)
        
if __name__=="__main__":
    print(checkunlock("mcesio"))