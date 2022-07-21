import socket
from aes.helper import int_from_bytes
from rsa.main import RSA
from aes.main import AES
from os import path
from converter.converter import int_to_bytes
import numpy as np

soc = socket.socket()
addr = ('localhost',8088)
soc.connect(addr)
print('Connected to server.')

# generate public and private keys
print('Generating RSA keys...')
rsa = RSA(256)
n, d, e = rsa.generate_keys()
filename = input("enter file name to receive: ")

# send public_key, e & filename
data = "\n".join([str(n), str(e), filename])
soc.send(data.encode('utf-8'))

# read data from server
data = b''
while True:
    print('hit!')
    part = soc.recv(4096)
    data += part
    if len(part) < 4096:
        break

# split data into cipherkey, iv & out from server
data = data.decode('latin1').split('\n\a\b\f\n\r\t\v\n\n')
cipherkey = int(data[0])
iv = [int(x) for x in data[1].split(' ')]
out = data[2].encode('latin1')

# decrypt cipherkey with RSA
key = rsa.decrypt(cipherkey, d, n)

# decrypt data using key with AES
aes = AES()
filename, ext = path.splitext(filename)
filename = filename + '-client' + ext
# convert key type from int to bytes
key = int_to_bytes(key)
aes.cbc_decrypt_file(out, filename, key, iv)
    
print("File has been received.")