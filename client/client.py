import socket

soc = socket.socket()
addr = ('localhost',8083)
soc.connect(addr)
print('Connected to server.')
# request for a file with name:
filename = input("file to request: ")
soc.send(filename.encode('utf-8'))
with soc,open(filename,'wb') as file:
    while True:
        recvfile = soc.recv(4096)
        if not recvfile: break
        file.write(recvfile)
print("File has been received.")