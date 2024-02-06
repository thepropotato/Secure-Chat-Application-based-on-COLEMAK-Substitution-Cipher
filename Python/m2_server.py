import socket
import rsa as rs
import test as secret
import test_rsa_mod as rsa
import COLEMAK as colemak

def server_program():
    host = socket.gethostname() # CHANGE TO REQUIRED SERVER IP ADDRESS
    port = 5000
    
    s_publickey, s_privatekey = rsa.genkey()

    server_socket = socket.socket()
    server_socket.bind((host, port))
    server_socket.listen(2)
    conn, address = server_socket.accept()
    print("Connection from: " + str(address))
    
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
            print("Public key sent !")
            cli_e = conn.recv(1024).decode()
            print("Client's public key recieved")
            clientkey = rs.PublicKey(int(cli_n), int(cli_e))
            print("CLIENT PUBLIC KEY :", clientkey)
        elif num == 2 :
            enc_colekey = conn.recv(1024)
            colekey = rs.decrypt(enc_colekey, s_privatekey)
            colekey = str(colekey)[2:len(colekey)+2]
            print("Decrypted Colekey recieved")
        num = num+1

    while True:
        data = conn.recv(1024).decode()
        safe_data = colemak.decrypt(data, colekey)
        if not data:
            break
        print("from connected user (Encrypted) : ", data)
        print("from connected user (Decrypted) : ", safe_data)
        message = input(' -> ')
        safe_message = colemak.encrypt(message, colekey)
        conn.send(safe_message.encode())

    conn.close()

if __name__ == '__main__':
    server_program()