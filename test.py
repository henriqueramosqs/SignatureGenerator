# Project test class
import unittest
from RSA import *

class TestSignaturesGeneratorClass(unittest.TestCase):

    def test_oaep_encode(self):
        msg =  b"Mensagem de teste"
        seed = b'\x00' * 32
        expected_output = oaep_encode(msg, enLen=128, seed=seed)
        self.assertEqual(oaep_encode(msg, enLen=128, seed=seed), expected_output)

    def test_oaep_decode(self):
        msg =  b"Mensagem de teste"
        seed = b'\x00' * 32
        expected_output = oaep_decode(oaep_encode(msg, enLen=128, seed=seed), enLen=128)
        self.assertEqual(oaep_decode(msg, enLen=128), expected_output)

    def test_chaves_geradas_com_pelo_menos_1024_bits(self):
        p = gen_prime()
        q = gen_prime()
        self.assertGreaterEqual(p.bit_length(), 1024)
        self.assertGreaterEqual(q.bit_length(), 1024)

if __name__ == "__main__":  
    unittest.main(verbosity=2)