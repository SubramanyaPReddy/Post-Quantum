# backend/routes/benchmark.py

from flask import Blueprint, jsonify
from backend.routes.keys import KEYS
from backend.utils import classical, hybrid, post_quantum
from backend.database import save_test_result
import time
import json

bp = Blueprint('benchmark', __name__)
FIXED_MESSAGE = "NIST benchmarking with RSA, Kyber, and Hybrid."

@bp.route('/run_benchmark', methods=['POST'])
def run_benchmark():
    results = []

    # --- ENCRYPTION ---

    # RSA
    rsa_ct, rsa_enc_time = classical.rsa_encrypt(KEYS['rsa'].publickey(), FIXED_MESSAGE)
    results.append({
        'type': 'encryption',
        'algorithm': 'RSA-3072',
        'time': rsa_enc_time,
        'size': len(rsa_ct),
        'security': '128 bits'
    })
    save_test_result('encryption', 'RSA-3072', FIXED_MESSAGE, rsa_enc_time, len(rsa_ct), encrypted_data=rsa_ct)

    # Kyber (via hybrid AES encapsulation only)
    kyber_result = hybrid.hybrid_encrypt(KEYS['ml_kem']['public_key'], FIXED_MESSAGE)
    aes_ct = kyber_result['aes']['ciphertext']
    kyber_enc_time = kyber_result['total_time']
    results.append({
        'type': 'encryption',
        'algorithm': 'ML-KEM-768',
        'time': kyber_enc_time,
        'size': len(aes_ct),
        'security': '192 bits'
    })
    save_test_result('encryption', 'ML-KEM-768', FIXED_MESSAGE, kyber_enc_time, len(aes_ct), encrypted_data=aes_ct)

    # Hybrid
    hybrid_enc_time = rsa_enc_time + kyber_enc_time
    results.append({
        'type': 'encryption',
        'algorithm': 'Hybrid (RSA+Kyber)',
        'time': hybrid_enc_time,
        'size': len(rsa_ct) + len(aes_ct),
        'security': '>=192 bits'
    })
    save_test_result('encryption', 'Hybrid (RSA+Kyber)', FIXED_MESSAGE, hybrid_enc_time, len(rsa_ct) + len(aes_ct))

    # --- SIGNATURE ---

    # RSA Sign
    rsa_sig, rsa_sign_time = classical.rsa_sign(KEYS['rsa'], FIXED_MESSAGE)
    results.append({
        'type': 'signature',
        'algorithm': 'RSA-3072',
        'time': rsa_sign_time,
        'size': len(rsa_sig),
        'security': '128 bits'
    })
    save_test_result('signing', 'RSA-3072', FIXED_MESSAGE, rsa_sign_time, len(rsa_sig), signature_data=rsa_sig)

    # Dilithium
    dilithium = post_quantum.ml_dsa_sign(KEYS['ml_dsa']['private_key'], FIXED_MESSAGE)
    results.append({
        'type': 'signature',
        'algorithm': 'ML-DSA-65',
        'time': dilithium['time'],
        'size': dilithium['size'],
        'security': '192 bits'
    })
    save_test_result('signing', 'ML-DSA-65', FIXED_MESSAGE, dilithium['time'], dilithium['size'], signature_data=dilithium['signature'])

    # Hybrid
    results.append({
        'type': 'signature',
        'algorithm': 'Hybrid (RSA+Dilithium)',
        'time': rsa_sign_time + dilithium['time'],
        'size': len(rsa_sig) + dilithium['size'],
        'security': '>=192 bits'
    })
    save_test_result('signing', 'Hybrid (RSA+Dilithium)', FIXED_MESSAGE,
                     rsa_sign_time + dilithium['time'], len(rsa_sig) + dilithium['size'])

    return jsonify({'results': results})
