import rsa
import COLEMAK as colemak
import binascii

def genkey():
    publicKey, privateKey = rsa.newkeys(512)
    return publicKey, privateKey

publicKey, privateKey = genkey()

def enc(message, key, colekey):
    encMessage = rsa.encrypt(message.encode(), key)
    print("-------- LEVEL 1 ENCRYPTION : ---------")
    print(encMessage)
    print(" ")
    print("-------- LEVEL 2 ENCRYPTION : ---------")
    encMessage_colemak = cole_enc(encMessage, colekey)
    print(encMessage_colemak)
    return encMessage_colemak

def dec(message, key, colekey):
    decMessage_colemak = cole_dec(message, colekey)
    print("-------- LEVEL 1 DECRYPTION : ---------")
    print(decMessage_colemak)
    print(" ")
    print("-------- LEVEL 2 DECRYPTION : ---------")
    decMessage = rsa.decrypt(decMessage_colemak, key).decode()
    print(decMessage)
    return decMessage  # string

def cole_enc (mes, key) :
    mes = byte_to_hex(mes)
    enc_mes = colemak.encrypt(mes, key)
    return enc_mes
    
def cole_dec (mes, key) :
    enc_mes = colemak.decrypt(mes, key)
    enc_mes_bytes = hex_to_byte(enc_mes)
    return enc_mes_bytes

def byte_to_hex (byte) :
    hex_representation = binascii.hexlify(byte).decode()
    return hex_representation
    
def hex_to_byte (hex) :
    normal_byte_string = binascii.unhexlify(hex)
    return normal_byte_string
