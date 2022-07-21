import socket
from rsa.main import RSA
from helper import int_to_bytes
soc = socket.socket()
soc.connect(('localhost',8082))

# generate public and private keys
print('Generating RSA keys...')
rsa_key_len = 1024
rsa = RSA(rsa_key_len)
public_key, private_key, e = rsa.generate_keys()
filename = input("enter file name to receive: ")

# send public_key, e & filename
data = "\n".join([str(public_key), str(e), filename])
soc.send(data.encode('utf-8'))

# get data
with soc, open(filename,'wb') as file:
    soc.send(filename.encode('utf-8'))
    while True:
        recvfile = soc.recv(4096)
        if not recvfile: break
        file.write(recvfile)
print("File has been received.")