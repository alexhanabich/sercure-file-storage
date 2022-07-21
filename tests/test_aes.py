import os
from random import getrandbits
THIS_DIR = os.path.dirname(os.path.abspath(__file__))

import unittest
from converter.converter import file_to_nparr, str_to_nparr, nparr_to_str
from aes.key_expansion import key_expansion
from aes.cipher import cipher, sub_bytes, mix_columns, shift_rows
from aes.helper import get_round_key, add_round_key, to_matrix, flatten
from aes.main import AES
import filecmp

class TestAES(unittest.TestCase):
    def test_key_expansion(self):
        key = str_to_nparr('2b7e151628aed2a6abf7158809cf4f3c')
        w = key_expansion(key)
        actual = nparr_to_str(w, 8)
        expected = ('2b7e151628aed2a6abf7158809cf4f3c' +
                    'a0fafe1788542cb123a339392a6c7605' +
                    'f2c295f27a96b9435935807a7359f67f' +
                    '3d80477d4716fe3e1e237e446d7a883b' +
                    'ef44a541a8525b7fb671253bdb0bad00' +
                    'd4d1c6f87c839d87caf2b8bc11f915bc' +
                    '6d88a37a110b3efddbf98641ca0093fd' +
                    '4e54f70e5f5fc9f384a64fb24ea6dc4f' +
                    'ead27321b58dbad2312bf5607f8d292f' +
                    'ac7766f319fadc2128d12941575c006e' +
                    'd014f9a8c9ee2589e13f0cc8b6630ca6')
        self.assertEqual(actual, expected)
    
    def test_get_round_key(self):
        key = str_to_nparr('2b7e151628aed2a6abf7158809cf4f3c')
        w = key_expansion(key)
        round_key = get_round_key(w, 0, 3)
        actual = nparr_to_str(flatten(round_key), 2)
        expected = '2b7e151628aed2a6abf7158809cf4f3c'
        self.assertEqual(actual, expected)


    def test_add_round_key(self):
        input = str_to_nparr('3243f6a8885a308d313198a2e0370734')
        key = str_to_nparr('2b7e151628aed2a6abf7158809cf4f3c')
        w = key_expansion(key)
        round_key = get_round_key(w, 0, 3)
        state = to_matrix(input)
        add_round_key(state, round_key)
        actual = nparr_to_str(flatten(state), 2)
        expected = '193de3bea0f4e22b9ac68d2ae9f84808'
        self.assertEqual(actual, expected)


    def test_sub_bytes(self):
        input = '193de3bea0f4e22b9ac68d2ae9f84808'
        state = to_matrix(str_to_nparr(input))
        sub_bytes(state)
        actual = nparr_to_str(flatten(state), 2)
        expected = 'd42711aee0bf98f1b8b45de51e415230'
        self.assertEqual(actual, expected)


    def test_shift_rows(self):
        input = 'd42711aee0bf98f1b8b45de51e415230'
        state = to_matrix(str_to_nparr(input))
        shift_rows(state)
        actual = nparr_to_str(flatten(state), 2)
        expected = 'd4bf5d30e0b452aeb84111f11e2798e5'
        self.assertEqual(actual, expected)

    
    def test_mix_columns(self):
        input = 'd4bf5d30e0b452aeb84111f11e2798e5'
        state = to_matrix(str_to_nparr(input))
        mix_columns(state)
        actual = nparr_to_str(flatten(state), 2)
        expected = '046681e5e0cb199a48f8d37a2806264c'
        self.assertEqual(actual, expected)


    def test_cipher(self):
        input = str_to_nparr('3243f6a8885a308d313198a2e0370734')
        key = str_to_nparr('2b7e151628aed2a6abf7158809cf4f3c')
        w = key_expansion(key)
        out = cipher(input, w)
        actual = nparr_to_str(flatten(out), 2)
        expected = '3925841d02dc09fbdc118597196a0b32'
        self.assertEqual(actual, expected)

    
    def test_aes_encrypt(self):
        input = str_to_nparr('3243f6a8885a308d313198a2e0370734')
        key = str_to_nparr('2b7e151628aed2a6abf7158809cf4f3c')
        aes = AES()
        cipher = aes.encrypt(input, key)
        actual = nparr_to_str(cipher, 2)
        expected = '3925841d02dc09fbdc118597196a0b32'
        self.assertEqual(actual, expected)

    def test_aes_decrypt(self):
        input = str_to_nparr('3925841d02dc09fbdc118597196a0b32')
        key = str_to_nparr('2b7e151628aed2a6abf7158809cf4f3c')
        aes = AES()
        cipher = aes.decrypt(input, key)
        actual = nparr_to_str(cipher, 2)
        expected = '3243f6a8885a308d313198a2e0370734'
        self.assertEqual(actual, expected)


    def test_cbc_aes_encrypt(self):
        input = str_to_nparr(('6bc1bee22e409f96e93d7e117393172a' +
                            'ae2d8a571e03ac9c9eb76fac45af8e51' +
                            '30c81c46a35ce411e5fbc1191a0a52ef' +
                            'f69f2445df4f9b17ad2b417be66c3710'))
        key = str_to_nparr('2b7e151628aed2a6abf7158809cf4f3c')
        iv = str_to_nparr('000102030405060708090a0b0c0d0e0f')
        aes = AES()
        cipher = aes.cbc_encrypt(input, key, iv)
        actual = nparr_to_str(cipher, 2)
        expected = ('7649abac8119b246cee98e9b12e9197d' +
                    '5086cb9b507219ee95db113a917678b2' +
                    '73bed6b8e3c1743b7116e69e22229516' +
                    '3ff1caa1681fac09120eca307586e1a7' +
                    'f434f467253f9a5969153be0552dd6ca')
        self.assertEqual(actual, expected)

    def test_cbc_aes_decrypt(self):
        input = str_to_nparr('7649abac8119b246cee98e9b12e9197d' +
                            '5086cb9b507219ee95db113a917678b2' +
                            '73bed6b8e3c1743b7116e69e22229516' +
                            '3ff1caa1681fac09120eca307586e1a7' +
                            'f434f467253f9a5969153be0552dd6ca')
        key = str_to_nparr('2b7e151628aed2a6abf7158809cf4f3c')
        iv = str_to_nparr('000102030405060708090a0b0c0d0e0f')
        aes = AES()
        plain = aes.cbc_decrypt(input, key, iv)
        actual = nparr_to_str(plain, 2)
        expected = ('6bc1bee22e409f96e93d7e117393172a' +
                    'ae2d8a571e03ac9c9eb76fac45af8e51' +
                    '30c81c46a35ce411e5fbc1191a0a52ef' +
                    'f69f2445df4f9b17ad2b417be66c3710')
        self.assertEqual(actual, expected)


    def test_file_read_write(self):
        # encrypt the file
        in_path = os.path.join(THIS_DIR, 'test.png')
        key = bytes('2b7e151628aed2a6abf7158809cf4f3c', 'utf-8')
        iv = str_to_nparr('000102030405060708090a0b0c0d0e0f')
        aes = AES()
        out = aes.cbc_encrypt_file(in_path, key, iv)
        
        # decrypt the file
        out_path = os.path.join(THIS_DIR, 'out.png')
        aes.cbc_decrypt_file(out, out_path, key, iv)
        self.assertTrue(filecmp.cmp(in_path, out_path))

        


if __name__ == '__main__':
    unittest.main()