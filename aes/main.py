import numpy as np
from aes.key_expansion import key_expansion
from aes.cipher import cipher
from aes.inv_cipher import inv_cipher
from aes.converter import file_to_nparr, nparr_to_file, str_to_nparr
from aes.helper import hex_print, split_arr
import random

from helper import int_from_bytes


BLOCK_SIZE = 16

class AES:
    def __pad(self, input: np.ndarray) -> np.ndarray:
        r = input.size%BLOCK_SIZE
        padding = [0x80]
        for i in range(BLOCK_SIZE-1-r):
            padding.append(0x00)
        return np.append(input, padding)


    def __unpad(self, input: np.ndarray) -> np.ndarray:
        pad_len = 0
        for i in range(len(input)-1, -1, -1):
            if input[i] == 0x00:
                pad_len += 1
            elif input[i] == 0x80:
                pad_len += 1
                break
        return np.resize(input, input.size-pad_len)


    def generate_key(self, n):
        return random.getrandbits(n)


    def generate_iv(self):
        return random.getrandbits(16)


    def encrypt(self, input: np.ndarray, key: np.ndarray) -> np.ndarray:
        # create key schedule
        w = key_expansion(key)
        # cipher
        return cipher(input, w)
        
    
    def decrypt(self, input: np.ndarray, key: np.ndarray) -> np.ndarray:
        # create key schedule
        w = key_expansion(key)
        # inv_cipher
        return inv_cipher(input, w)

    
    def ecb_encrypt(self, input: np.ndarray, key: np.ndarray) -> np.ndarray:
        input = self.__pad(input)
        cipher = []
        plain = split_arr(input, BLOCK_SIZE)
        for p_i in plain:
            c_i = self.encrypt(p_i, key)
            cipher.append(c_i)
        return np.concatenate(cipher)


    def ecb_decrypt(self, input: np.ndarray, key: np.ndarray) -> np.ndarray:
        plain = []
        cipher = split_arr(input, BLOCK_SIZE)
        for c_i in cipher:
            p_i = self.decrypt(c_i, key)
            plain.append(p_i)
        plain = np.concatenate(plain)
        return self.__unpad(plain)


    def cbc_encrypt(self, input: np.ndarray, key: np.ndarray, iv: np.ndarray) -> np.ndarray:
        input = self.__pad(input)
        cipher = []
        plain = split_arr(input, BLOCK_SIZE)
        p_1 = plain[0]
        c_1 = self.encrypt(p_1^iv, key)
        cipher.append(c_1)
        plain = plain[1:]
        # c_j = c_i-1
        c_j = c_1
        for p_i in plain:
            c_i = self.encrypt(p_i^c_j, key)
            cipher.append(c_i)
            c_j = c_i
        return np.concatenate(cipher)


    def cbc_decrypt(self, input: np.ndarray, key: np.ndarray, iv: np.ndarray) -> np.ndarray:
        plain = []
        cipher = split_arr(input, BLOCK_SIZE)
        c_1 = cipher[0]
        p_1 = self.decrypt(c_1, key)^iv
        plain.append(p_1)
        cipher = cipher[1:]
        # c_j = c_i-1
        c_j = c_1
        for c_i in cipher:
            p_i = self.decrypt(c_i, key)^c_j
            plain.append(p_i)
            c_j = c_i
        plain = np.concatenate(plain)
        return self.__unpad(plain)


    # def ecb_encrypt_file(self, in_file: str, key: bytes) -> bytes:
    #     ints = file_to_ints(in_file)
    #     key = np.array(list(key))
    #     aes = AES()
    #     ciphertext = aes.ecb_encrypt(ints, key)
    #     return bytes(ciphertext.tolist())


    # def ecb_decrypt_file(self, input: bytes, out_file: str, key: bytes) -> None:
    #     ints = np.array(list(input))
    #     key = np.array(list(key))
    #     aes = AES()
    #     plaintext = aes.ecb_decrypt(ints, key)
    #     ints_to_file(plaintext, out_file)


    def cbc_encrypt_file(self, in_file: str, key: bytes , iv: np.ndarray) -> bytes:
        ints = file_to_nparr(in_file)
        key = np.array(list(key))
        aes = AES()
        ciphertext = aes.cbc_encrypt(ints, key, iv)
        return bytes(ciphertext.tolist())


    def cbc_decrypt_file(self, input: bytes, out_file: str, key: bytes, iv: np.ndarray) -> None:
        ints = np.array(list(input))
        key = np.array(list(key))
        aes = AES()
        plaintext = aes.cbc_decrypt(ints, key, iv)
        nparr_to_file(plaintext, out_file)