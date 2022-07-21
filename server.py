import socket
from aes.helper import int_from_bytes
from aes.main import AES
from rsa.main import RSA
from converter.converter import int_to_bytes

soc = socket.socket()
soc.bind(('',8088))
soc.listen(1)

print('waiting for client to connect...')
threads = []

conn, addr = soc.accept()
print(f'connected to {addr[0]}:{addr[1]}')
with conn:
    # get data from stream and unpack
    data = conn.recv(4096).decode('utf-8').split('\n')
    n = int(data[0])
    e = int(data[1])
    filename = data[2]

    # generate 128 bit key and 16 bit iv for AES encryption
    aes = AES()
    key = aes.generate_key(128)
    iv = aes.generate_iv()

    # encrypt key using RSA using data from cli
    rsa = RSA()
    cipherkey = rsa.encrypt(key, e, n)

    # encrypt file using AES
    key = int_to_bytes(key)
    out = aes.cbc_encrypt_file(filename, key, iv)

    # send cipherkey, iv and out to client
    data = "\n\a\b\f\n\r\t\v\n\n".join([str(cipherkey), ' '.join(str(x) for x in iv), out.decode('latin1')])
    conn.sendall(data.encode('latin1'))

    print('file sent to ', addr)