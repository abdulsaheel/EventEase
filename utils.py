
import base64
import json
from cryptography.fernet import Fernet


# Hardcoded key (it should be a URL-safe base64-encoded 32-byte key)
key = b'wM04I6H-c_mYNZ8Kre7mly_VgbNvvyo3FGnlo-On9cA='
cipher_suite = Fernet(key)


def encrypt_string(plain_text):
    cipher_text = cipher_suite.encrypt(plain_text.encode())
    return cipher_text.decode()

def decrypt_string(cipher_text):
    plain_text = cipher_suite.decrypt(cipher_text.encode())
    return plain_text.decode()


def decode_base64(data):
    try:
        decoded_data = base64.b64decode(data)
        return json.loads(decoded_data)
    except Exception as e:
        print("Error decoding base64 data:", e)
        return None
    
