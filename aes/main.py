import numpy as np
from key_expansion import key_expansion
from cipher import cipher
from inv_cipher import inv_cipher
from converter import file_to_ints, ints_to_file, str_to_ints
from helper import hex_print, split_arr
import typing


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


    def cbc_encrypt(self, input: np.ndarray, key: np.ndarray, iv: bytes):
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


    def cbc_decrypt(self, input: np.ndarray, key: np.ndarray, iv: bytes):
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


    # in_file: str out_file: str, key: str, -> file
    def ecb_encrypt_file(self, in_file: str, out_file: str, key: str) -> typing.IO:
        ints = file_to_ints(in_file)
        key = str_to_ints(key)
        aes = AES()
        ciphertext = aes.ecb_encrypt(ints, key)
        ints_to_file(ciphertext, out_file)


    def ecb_decrypt_file(self, in_file: str, out_file: str, key: str) -> typing.IO:
        ints = file_to_ints(in_file)
        key = str_to_ints(key)
        aes = AES()
        plaintext = aes.ecb_decrypt(ints, key)
        ints_to_file(plaintext, out_file)


    def ecb_encrypt_text(self, txt: str, key: str) -> str:
        ints = str_to_ints(txt)
        key = str_to_ints(key)
        aes = AES()
        return aes.ecb_encrypt(ints, key)


    def ecb_decrypt_text(self, txt: str, key: str) -> str:
        ints = file_to_ints(txt)
        key = str_to_ints(key)
        aes = AES()
        return aes.ecb_decrypt(ints, key)


    def cbc_encrypt_file(self, in_file: str, out_file: str, key: str , iv: bytes) -> typing.IO:
        ints = file_to_ints(in_file)
        out_file = out_file
        key = str_to_ints(key)
        aes = AES()
        ciphertext = aes.cbc_encrypt(ints, key, iv)
        ints_to_file(ciphertext, out_file)


    def cbc_decrypt_file(self, in_file: str, out_file: str, key: str, iv: bytes) -> typing.IO:
        ints = file_to_ints(in_file)
        out_file = out_file
        key = str_to_ints(key)
        aes = AES()
        ciphertext = aes.cbc_decrypt(ints, key, iv)
        ints_to_file(ciphertext, out_file)


    def cbc_encrypt_text(self, txt: str, key: str) -> str:
        ints = str_to_ints(txt)
        key = str_to_ints(key)
        aes = AES()
        iv = bytearray(16)
        return aes.cbc_encrypt(ints, key, iv)


    def cbc_decrypt_text(self, txt: str, key: str) -> str:
        ints = file_to_ints(txt)
        key = str_to_ints(key)
        aes = AES()
        iv = bytearray(16)
        return aes.cbc_decrypt(ints, key, iv)