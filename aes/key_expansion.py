import numpy as np
from helper import get_sbox, rcon

# substitue bytes using sbox
def sub_word(word: bytes) -> bytes:
    b0 = (word>>24) & 0xFF
    b1 = (word>>16) & 0xFF
    b2 = (word>>8) & 0xFF
    b3 = word & 0xFF
    return get_sbox(b0)<<24 | get_sbox(b1)<<16 | get_sbox(b2)<<8 | get_sbox(b3)

# rotate the first byte to the last
def rot_word(word: bytes) -> bytes:
    b0 = (word>>24) & 0xFF
    b1 = (word>>16) & 0xFF
    b2 = (word>>8) & 0xFF
    b3 = word & 0xFF
    return b1<<24 | b2<<16 | b3<<8 | b0


def key_expansion(key: np.ndarray) -> np.ndarray:
    nb = 4
    nk = key.size // 4
    nr = nk + 6
    w = np.zeros((nb*(nr+1),), np.uint32)
    for i in range(nk):
        w[i] = key[4*i]<<24 | key[4*i+1]<<16 | key[4*i+2]<<8 | key[4*i+3]
    for i in range(nk,(nb*(nr+1))):
            temp = w[i-1]
            if (i%nk) == 0:
                temp = sub_word(rot_word(temp))^rcon[i//nk]
            elif (nk>6 and i%nk == 4):
                temp = sub_word(temp)
            w[i] = w[i-nk] ^ temp
    return w
