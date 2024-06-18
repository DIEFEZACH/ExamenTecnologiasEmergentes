import unittest
import hashlib
import time

# Función para encriptar con SHA1
def sha1_encrypt(text):
    return hashlib.sha1(text.encode('utf-8')).hexdigest()

class TestSHA1Encryption(unittest.TestCase):
    def test_sha1_encrypt(self):
        self.assertEqual(sha1_encrypt('English'), hashlib.sha1('English'.encode('utf-8')).hexdigest())
        self.assertNotEqual(sha1_encrypt('English'), hashlib.sha1('Spanish'.encode('utf-8')).hexdigest())
    
    def test_processing_time(self):
        start_time = time.time()
        sha1_encrypt('English')
        end_time = time.time()
        self.assertGreater(end_time - start_time, 0)

if __name__ == '__main__':
    unittest.main()

