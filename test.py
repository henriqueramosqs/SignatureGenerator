# Project test class
import unittest
from RSA import is_prime
from RSA import *

class TestSignaturesGeneratorClass(unittest.TestCase):

    def test_oape(self):
        msg =  b"Mensagem de teste"
        seed = b'\x00' * 32
        expected_output = oape_encode(msg, enLen=128, seed=seed)
        self.assertEqual(oape_encode(msg, enLen=128, seed=seed), expected_output)

if __name__ == "__main__":  
    unittest.main(verbosity=2)