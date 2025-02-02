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

if __name__ == "__main__":  
    unittest.main(verbosity=2)