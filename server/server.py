import socket
import sys

soc = socket.socket()
soc.bind(('',8083))
soc.listen(1)

print('waiting for client to connect...')
while True:
    conn,addr = soc.accept()
    print('connected to', addr)
    with conn:
        filename = conn.recv(1024).decode('utf-8')
        with open(filename, 'rb') as file:
            sendfile = file.read()
        conn.sendall(sendfile)
        print('file sent to ', addr)
