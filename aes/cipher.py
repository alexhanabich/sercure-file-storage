import numpy as np
from aes.helper import ff_mult, add_round_key, get_round_key, to_matrix, flatten, get_sbox
import logging

# substitute bytes with sbox
def sub_bytes(state: np.ndarray) -> None:
    for i in range(len(state)):
        for j in range(len(state[i])):
            state[i][j] = get_sbox(state[i][j])


# shift ith row by -i
def shift_rows(state: np.ndarray) -> None:
    for i in range(len(state)):
        state[i] = np.roll(state[i], -i)


# mix columns
def mix_columns(state: np.ndarray) -> None:
    for col in np.transpose(state):
        copy = np.copy(col)
        col[0] = ff_mult(2,copy[0]) ^ ff_mult(3,copy[1]) ^ copy[2] ^ copy[3]
        col[1] = copy[0] ^ ff_mult(2,copy[1]) ^ ff_mult(3,copy[2]) ^ copy[3]
        col[2] = copy[0] ^ copy[1] ^ ff_mult(2,copy[2]) ^ ff_mult(3,copy[3])
        col[3] = ff_mult(3,copy[0]) ^ copy[1] ^ copy[2] ^ ff_mult(2,copy[3])


# input: 128bit block, output: 128bit block
def cipher(input: np.ndarray, w: np.ndarray) -> np.ndarray:
    nb = 4
    nr = len(w)//4 - 1
    # make a copy so that the input is preserved
    input = np.copy(input)
    state = to_matrix(input)
    add_round_key(state, get_round_key(w, 0, nb-1))
    for i in range(1, nr):
        sub_bytes(state)
        shift_rows(state)
        mix_columns(state)
        add_round_key(state, get_round_key(w, i*nb, (i+1)*nb-1))
    sub_bytes(state)
    shift_rows(state)
    add_round_key(state,  get_round_key(w, nr*nb, (nr+1)*nb-1))
    return flatten(state)