import socket
import test_rsa_mod as rsa
import rsa as rs
import os
import test as secret

def install_missing_libraries():
    required_libraries = ['psutil','hashlib','platform','os','socket','uuid','json','time','rsa']
    for library in required_libraries:
        try:
            __import__(library)
        except ImportError:
            print(f"{library} library not found. Installing...")
            os.system(f'pip install {library}')

install_missing_libraries()

def client_program():
    host = socket.gethostname()
    port = 5000
    
    c_publickey, c_privatekey = rsa.genkey()

    client_socket = socket.socket()
    client_socket.connect((host, port))
    
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
            print("Public key sent !")
            ser_e = client_socket.recv(1024).decode()
            print("Server's public key recieved")
            serverkey = rs.PublicKey(int(ser_n), int(ser_e))
            print("SERVER PUBLIC KEY :", serverkey)
            colekey = secret.generate_device_fingerprint()
        elif num == 2 :
            client_socket.send(colekey.encode())
            print("Colekey sent")
        num = num+1

    message = input(" -> ")

    while message.lower().strip() != 'bye' and num != 0:
        safe_message = rsa.enc(message, serverkey, colekey)
        client_socket.send(safe_message.encode())
        data = client_socket.recv(1024).decode()
        safe_data = rsa.dec(data, c_privatekey, colekey)
        print('Received from server (Encrypted) : ', data)
        print('Received from server (Decrypted) : ', safe_data)
        message = input(" -> ")

    client_socket.close()

if __name__ == '__main__':
    client_program()
