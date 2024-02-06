from tkinter import *
from socket import *
import _thread
from tkinter import simpledialog
import test_rsa_mod as trm
import rsa as rs
from datetime import datetime
import test as secret

def get_server_ip():
    return simpledialog.askstring("Server IP", "Enter Server IP Address:")

server_ip = str(get_server_ip())
print(str(server_ip))

# initialize server connection
def initialize_client():
    # initialize socket
    client_socket = socket(AF_INET, SOCK_STREAM)
    # config details of server
    host = server_ip ## to use between devices in the same network eg.192.168.1.5
    port = 1234
    # connect to server
    client_socket.connect((host, port))
    return client_socket

# update the chat log
def update_chat(msg, state):
    global chatlog

    chatlog.config(state=NORMAL)
    # update the message in the window
    if state==0:
        chatlog.insert(END, datetime.now().strftime("%H:%M:%S") + ', YOU: ' + msg)
    else:
        chatlog.insert(END, datetime.now().strftime("%H:%M:%S") + ', SERVER: ' + msg)
    chatlog.config(state=DISABLED)
    # show the latest messages
    chatlog.yview(END)
    
c_publickey, c_privatekey = trm.genkey()
client_socket = initialize_client()
    
def keyexchange() :
    num = 0
    ser_e = 0
    ser_n = 0
    
    while num <= 2 :
        if num == 0 :
            ckey_n = str(c_publickey.n)
            client_socket.send(str(ckey_n).encode())
            ser_n = client_socket.recv(1024).decode()
            
        elif num == 1 :
            ckey_e = str(c_publickey.e)
            client_socket.send(str(ckey_e).encode())
            print("------------ CONNECTION ESTABLISHED ------------")
            print("Public key sent !")
            ser_e = client_socket.recv(1024).decode()
            print("Server's public key recieved")
            serverkey = rs.PublicKey(int(ser_n), int(ser_e))
        elif num == 2 :    
            colekey = secret.generate_device_fingerprint()
            client_socket.send(colekey.encode())
            print("Colekey sent !")
            print("------------------------------------------------")
        num = num+1
    return serverkey, colekey

serverkey, colekey = keyexchange()

# function to send message
def send():
    global textbox
    # get the message
    msg = textbox.get("0.0", END)
    # update the chatlog
    update_chat(msg, 0)
    newmsg = trm.enc(msg, serverkey, colekey)
    # send the message
    client_socket.send(newmsg.encode('ascii'))
    textbox.delete("0.0", END)

# function to receive message
def receive():
    while 1:
        try:
            data = client_socket.recv(1024)
            msg = data.decode('ascii')
            if msg != "":
                update_chat(trm.dec(msg, c_privatekey, colekey), 1)
        except:
            pass

def press(event):
    send()

# GUI function
def GUI():
    global chatlog
    global textbox

    # initialize tkinter object
    gui = Tk()
    # set title for the window
    gui.title("Client Chat")
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
    client_socket = initialize_client()
    GUI()