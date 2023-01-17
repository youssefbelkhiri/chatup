import json
from tkinter import *
from socket import *
from threading import *
import sqlite3

#=== Creation du base de données et des tables ===#
conn = sqlite3.connect('database.db')
cursor = conn.cursor()
cursor.execute('create table IF NOT EXISTS client(username TEXT primary key , password TEXT , email TEXT , firstname TEXT,lastname TEXT , tele TEXT )')
conn.commit()
conn.close()

conn = sqlite3.connect('database.db')
cursor = conn.cursor()
cursor.execute('create table IF NOT EXISTS msg(user TEXT , MSG TEXT )')
conn.commit()
conn.close()


usernames = []
clients = []
user_clients=[]


def gestion_msg(client, addr):
    while True:
        #=================== Recevoir des données ===========================#
        message=client.recv(1024).decode("utf-8")
        data=message.split(',')

        #=== Pour les données de création du compte ===#
        if data[0] == "user_data":
            if data[1]=="" or data[2]=="" or data[3]=="" or data[4]=="" or data[5]=="" or data[6]=="":
                client.send("error".encode())    
            else :
                client.send("confirm".encode())    
                conn = sqlite3.connect("database.db")
                cursor=conn.cursor()
                cursor.execute("insert into client (username,password,email,firstname,lastname,tele) values (?,?,?,?,?,?)",(data[1],data[2],data[3],data[4],data[5],data[6]))
                conn.commit()
                conn.close()
                user_reg=data[1]
                usernames.append(user_reg)
                user_clients.append((user_reg,client))

        #=== Pour les données d'authentification ===#
        elif data[0]=="user_login":
            if data[1]=="" or data[2]=="":
                client.send("error".encode())
            else:
                conn=sqlite3.connect("database.db")
                cursor=conn.cursor()
                cursor.execute("select * from client where username=? and password=? ",(data[1],data[2]))
                result=cursor.fetchone()
                if result==None:
                    client.send("incorrect".encode())
                else:
                    client.send("confirm".encode())
                    user=data[1]
                    usernames.append(user)
                    user_clients.append((user,client))
                conn.commit()
                conn.close()

        #=== Pour l'historique ===#
        elif data[0] =="historique":
            conn=sqlite3.connect('database.db')
            cursor=conn.cursor()
            cursor.execute('select * from msg')
            results=cursor.fetchall()
            if results:
                result = json.dumps(results)
                client.send(result.encode())
            else:
                client.send("Aucun message trouvé !".encode()) 

        #=== Pour les messages ===#  
        else:
            msg=message.split(':')

            #=== Pour la listes des utilisateurs connectés ===#    
            if len(msg)>1 and msg[1]=="online":
                for i in usernames :
                    client.send(f'{i}\n'.encode()) 

            #=== Pour le chat privés ===#           
            elif len(msg)>1 and msg[1].startswith("to"):
                prv=msg[1].split('@')
                to=prv[1].split(".")[0]
                msg_prv=prv[1].split(".")[1]
                for user in user_clients:
                    if user[0] == to: 
                        user[1].send(f"{msg[0]}(prv):{msg_prv}\n".encode("utf-8"))   

            #=== Pour la diffusion des messages aux utilisateurs ===#    
            else:
                conn=sqlite3.connect('database.db')
                cursor=conn.cursor()
                cursor.execute('insert into msg(user,MSG) values (?,?)',(msg[0],msg[1]))
                conn.commit()
                conn.close()
                print(f"{addr}: "+message)
                for cmp in clients:
                    if cmp is not client:
                        cmp.send(f'{message}\n'.encode("utf-8"))
                if not message:
                    break 

    client.close()
    clients.remove(client)


serveur = Tk()
serveur.title("Instant Messaging : Registre") #Donner un titre
serveur.geometry("500x500")        #Controler le largeur et la longuer       
serveur.resizable(False,False)     #Refuser l'acces au changement des longuer du fenetre
serveur.config(background="silver")#Changer la couleur du background  
serveur.iconbitmap("img/icon.ico")
server_text=Text(serveur,width=55)
server_text.configure(state='disabled')
server_text.configure(state='normal')
server_text.insert(END,"Le serveur est en attend des connexions du client !")
server_text.configure(state='disabled')
server_text.place(x=10,y=10)
host = '127.0.0.1'
port = 4444
server = socket(AF_INET, SOCK_STREAM)
server.bind((host, port))
server.listen()
serveur.mainloop()
while True:
    client, addr = server.accept()
    server_text.configure(state='normal')
    server_text.inser(END,"\n"+"Connecte avec:"+addr)
    server_text.configure(state='disabled')
    print(f"Connecte avec {str(addr)}")
    clients.append(client)
    thread = Thread(target=gestion_msg, args=(client, addr,))
    #thread.daemon = True
    thread.start()

   
#========================================== FIN ==========================================#
