import socket
from rsa.main import RSA
from aes.main import AES
from os import path
from helper import int_to_bytes

soc = socket.socket()
addr = ('localhost',8081)
soc.connect(addr)
print('Connected to server.')

# generate public and private keys
print('Generating RSA keys...')
rsa = RSA(256)
public_key, private_key, e = rsa.generate_keys()
filename = input("enter file name to receive: ")

# send public_key, e & filename
data = "\n".join([str(public_key), str(e), filename])
soc.send(data.encode('utf-8'))

# get cipherkey and iv from server
data = soc.recv(1024).decode('utf-8').split('\n')
print(data)
cipherkey = int_to_bytes(int(data[0]))
iv = int_to_bytes(int(data[1]))

# decrypt cipherkey with RSA
key = rsa.decrypt(cipherkey, private_key, public_key)
print(key)

# get data 
data = b''
while True:
    part = soc.recv(4096)
    data += part
    if len(part) < 4096:
        break

# decrypt data using key with AES
aes = AES()
filename, ext = path.splitext(filename)
filename = filename + 'client' + ext
aes.cbc_decrypt_file(data, filename, key, iv)
    
print("File has been received.")