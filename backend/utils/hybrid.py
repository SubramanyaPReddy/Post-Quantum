# backend/utils/hybrid.py

from backend.utils.post_quantum import ml_kem_encapsulate, ml_kem_decapsulate
from backend.utils.classical import aes_encrypt, aes_decrypt
import time

def hybrid_encrypt(public_key, message: str):
    start = time.time()
    kem = ml_kem_encapsulate(public_key)
    key_bytes = kem['shared_secret'].to_bytes(32, 'big')
    aes_result = aes_encrypt(key_bytes, message)
    total_time = time.time() - start
    return {
        'encapsulated_key': str(kem['encapsulated_key']),
        'aes': aes_result,
        'total_time': total_time
    }

def hybrid_decrypt(private_key, encapsulated_key: int, aes_data):
    start = time.time()
    secret, _ = ml_kem_decapsulate(private_key, encapsulated_key)
    key_bytes = secret.to_bytes(32, 'big')
    plaintext, _ = aes_decrypt(
        key_bytes,
        aes_data['ciphertext'],
        aes_data['tag'],
        aes_data['nonce']
    )
    return plaintext, time.time() - start
