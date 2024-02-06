from tkinter import *
from socket import *
import socket as sock
import _thread
from tkinter import simpledialog
import test_rsa_mod as trm
import rsa as rs
from datetime import datetime
import test as secret

def show_ip ():
    host = sock.gethostbyname(sock.gethostname())
    mess = f"Share this IP address with your client:\n\n{host}:\n\nPress OK when done !"
    simpledialog.messagebox.showinfo("Dialog Box", mess)

show_ip()

# initialize server connection
def initialize_server():
    # initialize socket
    s = socket(AF_INET, SOCK_STREAM)
    # config details of server
    host = sock.gethostbyname(sock.gethostname())
    port = 1234
    # initialize server
    s.bind((host, port))
    # set no. of clients
    s.listen(1)
    
    # accept the connection from client
    conn, addr = s.accept()
    return conn, addr

# update the chat log
def update_chat(msg, state):
    global chatlog
    chatlog.config(state=NORMAL)
    # update the message in the window
    if state==0:
        chatlog.insert(END, datetime.now().strftime("%H:%M:%S") + ', YOU: ' + msg)
    else:
        chatlog.insert(END, datetime.now().strftime("%H:%M:%S") + ', CLIENT: ' + msg)
    chatlog.config(state=DISABLED)
    # show the latest messages
    chatlog.yview(END)

s_publickey, s_privatekey = trm.genkey()    
conn, addr = initialize_server()

def keyexchange(conn):
    num = 0
    cli_e = 0
    cli_n = 0
    
    while num <= 2 :
        if num == 0 :
            skey_n = s_publickey.n
            conn.send(str(skey_n).encode())
            cli_n = conn.recv(1024).decode()
            
        elif num == 1 :
            skey_e = s_publickey.e
            conn.send(str(skey_e).encode())
            print("------------ CONNECTION ESTABLISHED ------------")
            print("Public key sent !")
            cli_e = conn.recv(1024).decode()
            print("Client's public key recieved")
            clientkey = rs.PublicKey(int(cli_n), int(cli_e))
        elif num == 2 :
            colekey = conn.recv(1024).decode()
            print("Colekey recieved !")
            print("------------------------------------------------")
        num = num+1
    return clientkey, colekey

clientkey, colekey = keyexchange(conn)

# function to send message
def send():
    global textbox
    # get the message
    msg = textbox.get("0.0", END)
    # update the chatlog
    update_chat(msg, 0)
    newmsg = trm.enc(msg, clientkey, colekey)
    # send the message
    conn.send(newmsg.encode('ascii'))
    textbox.delete("0.0", END)

# function to receive message
def receive():
    while 1:
        data = conn.recv(1024)
        msg = data.decode('ascii')
        update_chat(trm.dec(msg, s_privatekey, colekey), 1)

def press(event):
    send()

# GUI function
def GUI():
    global chatlog
    global textbox

    # initialize tkinter object
    gui = Tk()
    # set title for the window
    gui.title("Server Chat")
    # set size for the window
    gui.geometry("380x430")
    
    # Create a canvas for the background
    canvas = Canvas(gui, width=380, height=430)
    canvas.pack()

    # text space to display messages
    chatlog = Text(gui, bg='black', fg='white')
    chatlog.config(state=DISABLED)

    # button to send messages
    sendbutton = Button(gui, bg='orange', fg='black', text='SEND', command=send)

    # textbox to type messages
    textbox = Text(gui, bg='grey', fg='black')

    # place the components in the window
    chatlog.place(x=6, y=6, height=386, width=370)
    textbox.place(x=6, y=401, height=20, width=265)
    sendbutton.place(x=300, y=401, height=20, width=50)

    # bind textbox to use ENTER Key
    textbox.bind("<KeyRelease-Return>", press)

    # create thread to capture messages continuously
    _thread.start_new_thread(receive, ())

    # to keep the window in loop
    gui.mainloop()


if __name__ == '__main__':
    chatlog = textbox = None
    conn, addr = initialize_server()
    GUI()
