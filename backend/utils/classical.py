# backend/utils/classical.py

from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP, AES
from Crypto.Hash import SHA256
from Crypto.Signature import pkcs1_15
from Crypto.Random import get_random_bytes
import base64
import time

def generate_rsa_key():
    start = time.time()
    key = RSA.generate(3072)
    return key, time.time() - start

def rsa_encrypt(public_key, message: str):
    start = time.time()
    cipher = PKCS1_OAEP.new(public_key)
    ciphertext = cipher.encrypt(message.encode())
    return base64.b64encode(ciphertext).decode(), time.time() - start

def rsa_decrypt(private_key, ciphertext_b64: str):
    start = time.time()
    ciphertext = base64.b64decode(ciphertext_b64)
    cipher = PKCS1_OAEP.new(private_key)
    plaintext = cipher.decrypt(ciphertext).decode()
    return plaintext, time.time() - start

def rsa_sign(private_key, message: str):
    start = time.time()
    h = SHA256.new(message.encode())
    signature = pkcs1_15.new(private_key).sign(h)
    return base64.b64encode(signature).decode(), time.time() - start

def rsa_verify(public_key, message: str, signature_b64: str):
    start = time.time()
    h = SHA256.new(message.encode())
    signature = base64.b64decode(signature_b64)
    try:
        pkcs1_15.new(public_key).verify(h, signature)
        return True, time.time() - start
    except Exception:
        return False, time.time() - start

def generate_aes_key():
    return get_random_bytes(32)  # AES-256

def aes_encrypt(key, message: str):
    start = time.time()
    cipher = AES.new(key, AES.MODE_GCM)
    ciphertext, tag = cipher.encrypt_and_digest(message.encode())
    return {
        'ciphertext': base64.b64encode(ciphertext).decode(),
        'tag': base64.b64encode(tag).decode(),
        'nonce': base64.b64encode(cipher.nonce).decode(),
        'encryption_time': time.time() - start
    }

def aes_decrypt(key, ciphertext_b64, tag_b64, nonce_b64):
    start = time.time()
    ciphertext = base64.b64decode(ciphertext_b64)
    tag = base64.b64decode(tag_b64)
    nonce = base64.b64decode(nonce_b64)
    cipher = AES.new(key, AES.MODE_GCM, nonce=nonce)
    plaintext = cipher.decrypt_and_verify(ciphertext, tag)
    return plaintext.decode(), time.time() - start
