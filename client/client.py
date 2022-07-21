import socket
from rsa.main import RSA

soc = socket.socket()
addr = ('localhost',8083)
soc.connect(addr)
print('Connected to server.')

# generate public and private keys
rsa = RSA()
public_key, private_key, e = rsa.generate_keys()
print('Public key: ', public_key)
print('Private key: ', private_key)

# send public key, e and filename to server:
soc.send(public_key.encode('utf-8'))
soc.send(e.encode('utf-8'))
filename = input("File to request: ")
soc.send(filename.encode('utf-8'))

# get cipherkey and iv from server
cipherkey = soc.recv(1024)
iv = soc.recv(1024)

with soc,open(filename,'wb') as file:
    while True:
        recvfile = soc.recv(4096)
        if not recvfile: break
        file.write(recvfile)
print("File has been received.")