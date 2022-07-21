# import random
# from aes.helper import int_from_bytes, int_to_bytes
# from rsa.helper import mod_exp
# from rsa.main import RSA


# msg  = 22789175765697472253491166474461999395801490918951211686960257236951036736355
# # print(msg)
# rsa = RSA(256)
# n, d, e = rsa.generate_keys()

# # cipher = rsa.encrypt(msg, e, n)
# # print(cipher)
# # plain = rsa.decrypt(msg, d, n)
# # print(plain)


# n = 75791700976404142349050580651340657677331720031876467534104495313168041858813
# d = 48093041744430515033151005492571411418688647831821578491462472795478396965753
# e = 65537

# cipher = rsa.encrypt(msg, e, n)
# print(cipher)

# print(pow(msg, e, n))
# print('')
# print(mod_exp(msg, e, n))

# expected = 12757570742416843470610345964449332067300877531055493523085322184270178015131
from aes.main import AES
import numpy as np

aes = AES()
iv = aes.generate_iv()
print(iv)
s = ' '.join(str(x) for x in iv)
print(s)

r = [int(x) for x in s.split(' ')]
print(r)

