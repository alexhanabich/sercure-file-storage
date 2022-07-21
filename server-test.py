from fileinput import filename
import socket
from helper import int_from_bytes

soc = socket.socket()
soc.bind(('',8082))
soc.listen(1)

print('waiting for connection...')
with soc:
    con,addr = soc.accept()
    print('server connected to',addr)
    with con:
        data = con.recv(4096).decode('utf-8').split('\n')
        public_key = int(data[0])
        e = int(data[1])
        filename = data[2]

        with open(filename, 'rb') as file:
            sendfile = file.read()
        con.sendall(sendfile)
        print('file sent')