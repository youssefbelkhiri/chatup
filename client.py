from socket import *
from threading import *
from tkinter import *
from tkinter import messagebox


host = '127.0.0.1'
port = 4444

client = socket(AF_INET, SOCK_STREAM)
client.connect((host, port))

#========= Creation de la fentre registre =========#
def fen_registre():
    #=== Envoyer au serveur les données entrées par le client lors de création du compte ==#
    def user_data() :
        nom=nom_entry.get()
        prenom=prenom_entry.get()
        email=email_entry.get()
        username=username_entry.get()
        password=password_entry.get()
        tele=tele_entry.get()
        data = f"user_data,{username},{password},{email},{nom},{prenom},{tele}"
        client.send(data.encode())

    #=== Confirmation d'existence d'un champ vide ===#
    def conf_registre():
        info=client.recv(1024).decode()
        if  info=="error":
            messagebox.showerror("error","Entrez vos données !")
        # elif info=="duplcate":
        #     messagebox.showerror("error","username existe déja")    
        else:
            username=username_entry.get()
            chat(username)  

    #=== Fonction de la boutton Créer un compte ==#
    def send_data():
        user_data()
        conf_registre()


    fen_authentification.destroy()
    fen_registre = Tk()
    fen_registre.title("Instant Messaging : Registre") #Donner un titre
    fen_registre.geometry("500x500")        #Controler le largeur et la longuer       
    fen_registre.resizable(False,False)     #Refuser l'acces au changement des longuer du fenetre
    fen_registre.config(background="silver")#Changer la couleur du background  
    fen_registre.iconbitmap("img/icon.ico") #Changer l'incone du fenetre

    titre_registre = Label(fen_registre, text="Création d'un nouveau compte" , fg='black', bg='silver', font=('Cambria', 20))
    titre_registre.place(x=90,y=10) #Insérer le texte

    nom_label = Label(fen_registre, text='Nom: ', fg='black', bg='silver', font=('Courier',15))
    nom_label.place(x=10, y=60)
    nom_entry = Entry(fen_registre, width=30)
    nom_entry.place(x=180,y=64) #Insérer la zone de texte

    prenom_label = Label(fen_registre, text='Prénom: ', fg='black', bg='silver', font=('Courier',15))
    prenom_label.place(x=10, y=110)
    prenom_entry = Entry(fen_registre, width=30)
    prenom_entry.place(x=180,y=114)

    email_label = Label(fen_registre, text='E-mail: ', fg='black', bg='silver', font=('Courier',15))
    email_label.place(x=10, y=160)
    email_entry = Entry(fen_registre, width=30)
    email_entry.place(x=180,y=164)

    username_label = Label(fen_registre, text='USERNAME: ', fg='black', bg='silver', font=('Courier',15))
    username_label.place(x=10, y=210)
    username_entry = Entry(fen_registre, width=30)
    username_entry.place(x=180,y=214)

    password_label = Label(fen_registre, text='PASSWORD: ', fg='black', bg='silver', font=('Courier',15))
    password_label.place(x=10, y=260)
    password_entry = Entry(fen_registre, width=30)
    password_entry.place(x=180,y=264)

    tele_label = Label(fen_registre, text='N°Télé: ', fg='black', bg='silver', font=('Courier',15))
    tele_label.place(x=10, y=310)
    tele_entry = Entry(fen_registre, width=30)
    tele_entry.place(x=180,y=314)

    créer_compte_bt = Button(fen_registre, text='Créer un compte', fg='black', bg='white', font=40, width=15, justify='center',command=send_data)
    créer_compte_bt.place(x=180, y=360) #Ajouter une boutton

    menubar1 = Menu(fen_registre)
    f1 = Menu(menubar1)
    f1.add_command(label='New')
    f1.add_command(label='New file')
    f1.add_command(label='Open')
    f1.add_command(label='Save')
    f1.add_command(label='Save As')
    menubar1.add_cascade(label='File',menu=f1)
    f2 = Menu(menubar1)
    menubar1.add_cascade(label='Options',menu=f2)
    f3 = Menu(menubar1)
    menubar1.add_cascade(label='Edit',menu=f3)
    f4 = Menu(menubar1)
    menubar1.add_cascade(label='Help',menu=f4)
    fen_registre.config(menu=menubar1) #Ajouter des menubars

    fen_registre.mainloop() #Executer la fenetre


#=== Creation de la fenetre de chat ===#
def chat(user):
    #== Demande d'hitorique des messages ==#
    def historique():
        client.send(f"historique,{user}".encode())

    #== Envoie des messages ==#
    def Send_Msg():
        client_msg = ecrire_msg_entry.get()
        txtMessages.configure(state='normal')
        txtMessages.insert(END, "\n" + "Vous: "+ client_msg)
        txtMessages.configure(state='disabled')
        msg=f'{user}:{client_msg}'
        client.send(msg.encode())
        ecrire_msg_entry.delete(0, "end")

    #== Recevoir des donées du serveur ==#
    def Recv_Msg():
        while True:
            server_msg = client.recv(1024).decode("utf-8")
            print(server_msg)
            txtMessages.configure(state='normal')
            txtMessages.insert(END, "\n"+server_msg)
            txtMessages.configure(state='disabled')

    chat = Tk()
    chat.title('Instant Messaging: Salon de chat')
    chat.geometry('500x550')
    chat.config(background='Azure')
    chat.resizable(False,False)
    chat.iconbitmap("img/icon.ico")  

    txtMessages = Text(chat, width=55)
    txtMessages.configure(state='disabled')
    txtMessages.place(x=10, y=10)

    ecrire_msg_label = Label(chat, text='Ecrire un message :', fg='black', bg='Azure', font=('Cambria',14))
    ecrire_msg_label.place(x=10,y=440)
    ecrire_msg_entry = Entry(chat, width=40)
    ecrire_msg_entry.place(x=190,y=446)

    envoyer_bt = Button(chat, text='Envoyer', command=Send_Msg, fg='black', bg='white', justify='center')
    envoyer_bt.place(x=440, y=442)

    historique_bt = Button(chat, text='Historique', bg='white', fg='black', font=40, width=15, justify='center',command=historique)
    historique_bt.place(x=300, y=480)

    deconnecter_bt = Button(chat, text='Déconnecter', command=chat.destroy, fg='black', bg='white', font=40, width=15, justify='center')
    deconnecter_bt.place(x=30, y=480)

    menubar_chat = Menu(chat)
    f1_chat = Menu(menubar_chat)
    menubar_chat.add_cascade(label='Créer un salon',menu=f1_chat)
    f2_chat = Menu(menubar_chat)
    menubar_chat.add_cascade(label='Bloquer un ami',menu=f2_chat)
    f3_chat = Menu(menubar_chat)
    menubar_chat.add_cascade(label='Aide',menu=f3_chat)
    f4_chat = Menu(menubar_chat)
    menubar_chat.add_cascade(label='A propos',menu=f4_chat)
    chat.config(menu=menubar_chat)

    recvThread = Thread(target=Recv_Msg)
    recvThread.start()

    chat.mainloop()

#== Envoyer au serveur les données entrées par le client lors d'authentification ==#
def login():
    user=username_entry.get()
    passw=password_entry.get()
    data=f"user_login,{user},{passw}"
    client.send(data.encode())

#=== Confirmation de sing up ===#
def confirmation():
    info = client.recv(1024).decode()
    if info=="error":
        messagebox.showerror("error","svp! Entrez vos données")
    elif info=="incorrect":
        messagebox.showerror("error","username ou password est incorrect !")    
    else:
        chat(username_entry.get())  

#=== Fonction de la boutton Se connecter ==#
def se_connecter():
    login() 
    confirmation()


fen_authentification = Tk()
fen_authentification.title("Instant Messaging : Authentification")     
fen_authentification.geometry("400x500")        
fen_authentification.resizable(False,False)     
fen_authentification.config(background="gray")        
fen_authentification.iconbitmap("img/icon.ico")       

titre_auth = Label(fen_authentification, text="Authentification", fg='white', bg='gray', font=('Cambria', 20))
titre_auth.place(x=100,y=10)

img_auth = PhotoImage(file="img/c_r_img.png") #pour ajouter l'image
img_auth_label = Label(fen_authentification, image=img_auth)
img_auth_label.place(x=70,y=60)

username_label = Label(fen_authentification, text="USERNAME: ", fg='white', bg='gray', font=('Courier',15))
username_label.place(x=20, y=300)
username_entry = Entry(fen_authentification, width=30)
username_entry.place(x=134,y=305)

password_label = Label(fen_authentification, text="PASSWORD: ", fg='white', bg='gray', font=('Courier',15))
password_label.place(x=20, y=340)
password_entry = Entry(fen_authentification, width=30,show='*')
password_entry.place(x=134,y=345)

seconnecter_bt = Button(fen_authentification, text="Se Connecter", command=se_connecter, fg='black', bg='white', font=40, width=15, justify='center')
seconnecter_bt.place(x=110, y=390)

passage_registre_label = Label(fen_authentification, text="Vous n'avez pas un compte ?", fg='white', bg='gray', font=('Arial',12))
passage_registre_label.place(x=20, y=460)
passage_registre_bt = Button(fen_authentification, text="Créer un compte", command=fen_registre, fg='black', bg='white')
passage_registre_bt.place(x=235, y=460)

fen_authentification.mainloop()

#========================================== FIN ==========================================#
