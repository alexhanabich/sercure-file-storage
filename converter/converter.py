import numpy as np

def file_to_nparr(filename):
    with open(filename, 'rb') as f:
        content = f.read()
    return np.array(list(content))


def nparr_to_file(ints, filename):
    ints = ints.tolist()
    with open(filename, 'wb+') as f:
        f.write(bytes(ints))


def str_to_nparr(str):
    n = 2
    chunks = [str[i:i+n] for i in range(0, len(str), n)]
    return np.array([int(x, 16) for x in chunks])


def nparr_to_str(ints, n_chr):
    strs = [hex(x)[2:].zfill(n_chr) for x in ints]
    return ''.join(strs)


def int_to_bytes(x: int) -> bytes:
    return x.to_bytes((x.bit_length() + 7) // 8, 'big')
    
def int_from_bytes(xbytes: bytes) -> int:
    return int.from_bytes(xbytes, 'big')