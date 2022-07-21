import numpy as np
from helper import get_inv_sbox, ff_mult, to_matrix, get_round_key, add_round_key, flatten

# substitute bytes with inv_sbox
def inv_sub_bytes(state: np.ndarray) -> None:
    for i in range(len(state)):
        for j in range(len(state[i])):
            state[i][j] = get_inv_sbox(state[i][j])


# shift ith row by i
def inv_shift_rows(state: np.ndarray) -> None:
    for i in range(len(state)):
        state[i] = np.roll(state[i], i)


# mix columns
def inv_mix_columns(state: np.ndarray) ->None:
    for col in np.transpose(state):
        copy = np.copy(col)
        col[0] = ff_mult(0x0e,copy[0]) ^ ff_mult(0x0b,copy[1]) ^ ff_mult(0x0d,copy[2]) ^ ff_mult(0x09,copy[3])
        col[1] = ff_mult(0x09,copy[0]) ^ ff_mult(0x0e,copy[1]) ^ ff_mult(0x0b,copy[2]) ^ ff_mult(0x0d,copy[3])
        col[2] = ff_mult(0x0d,copy[0]) ^ ff_mult(0x09,copy[1]) ^ ff_mult(0x0e,copy[2]) ^ ff_mult(0x0b,copy[3])
        col[3] = ff_mult(0x0b,copy[0]) ^ ff_mult(0x0d,copy[1]) ^ ff_mult(0x09,copy[2]) ^ ff_mult(0x0e,copy[3])


# get round key from key schedule
def inv_cipher(input: np.ndarray, w: np.ndarray) -> np.ndarray:
    nb = 4
    nr = len(w)//4 - 1
    input = np.copy(input)
    state = to_matrix(input)
    add_round_key(state,  get_round_key(w, nr*nb, (nr+1) * nb-1))
    for i in range(nr-1, 0, -1):
        inv_shift_rows(state)
        inv_sub_bytes(state)
        add_round_key(state, get_round_key(w, i*nb, (i+1)*nb-1))
        inv_mix_columns(state)
    inv_shift_rows(state)
    inv_sub_bytes(state)
    add_round_key(state,  get_round_key(w, 0, nb - 1))
    return flatten(state)