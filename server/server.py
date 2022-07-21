import socket
import threading
import os
from aes.main import AES
from rsa.main import RSA

def handle_client(conn, addr):
    with conn:
        # get public key, expoenent & filename from client
        public_key = conn.recv(1024).decode('utf-8')
        e = conn.recv(1024).decode('utf-8')
        filename = conn.recv(1024).decode('utf-8')

        # generate 128 bit key and 16 bit iv for AES encryption
        aes = AES()
        key = aes.generate_key(128)
        iv = aes.generate_iv()

        # encrypt key using RSA
        rsa = RSA()
        cipherkey = rsa.encrypt(key, e, public_key)

        # send cipherkey and iv to client
        conn.send(cipherkey)
        conn.send(iv)

        # encrypt file using AES
        filename, ext = os.path.splitext(filename)
        outfile = filename + addr + ext
        out = aes.cbc_encrypt_file(filename, outfile, key, iv)

        # send encrypted file
        conn.sendall(out)
        print('file sent to ', addr)


soc = socket.socket()
soc.bind(('',8083))
soc.listen(1)

print('waiting for client to connect...')
threads = []

while True:
    conn, addr = soc.accept()
    print(f'connected to {addr[0]}:{addr[1]}')
    handle_client(conn)
    t = threading.Thread(target=handle_client, args=(conn, addr))
    t.start
    threads.append(t)
