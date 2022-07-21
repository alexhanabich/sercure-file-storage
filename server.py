import socket
from aes.main import AES
from rsa.main import RSA
from helper import int_from_bytes, int_to_bytes

soc = socket.socket()
soc.bind(('',8081))
soc.listen(1)

print('waiting for client to connect...')
threads = []

conn, addr = soc.accept()
print(f'connected to {addr[0]}:{addr[1]}')
with conn:
    # get data from stream and unpack
    data = conn.recv(4096).decode('utf-8').split('\n')
    public_key = int(data[0])
    e = int(data[1])
    filename = data[2]
    print(public_key, e, filename)

    # generate 128 bit key and 16 bit iv for AES encryption
    aes = AES()
    key = int_to_bytes(aes.generate_key(128))
    iv = int_to_bytes(aes.generate_iv())


    # encrypt key using RSA
    rsa = RSA()
    cipherkey = rsa.encrypt(key, e, public_key)

    # send cipherkey and iv to client
    data = "\n".join([str(cipherkey), str(iv)])
    conn.send(data.encode('utf-8'))

    # encrypt file using AES
    out = aes.cbc_encrypt_file(filename, key, iv)

    # send encrypted file
    conn.sendall(out)
    print('file sent to ', addr)