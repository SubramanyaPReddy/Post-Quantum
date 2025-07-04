from flask import Blueprint, request, jsonify
from backend.routes.keys import KEYS
from backend.utils import classical, hybrid
from backend.database import save_test_result

bp = Blueprint('multiencrypt', __name__)

@bp.route('/encrypt_all', methods=['POST'])
def encrypt_all():
    data = request.json
    message = data.get("message", "")
    if not message:
        return jsonify({"error": "Message is empty"}), 400

    results = []

    # RSA
    ct_rsa, time_rsa = classical.rsa_encrypt(KEYS['rsa'].publickey(), message)
    results.append({
        'algorithm': 'RSA-3072',
        'time': time_rsa,
        'size': len(ct_rsa),
        'security': '128 bits'
    })
    save_test_result('encryption', 'RSA-3072', message, time_rsa, len(ct_rsa), encrypted_data=ct_rsa)

    # Kyber
    kem = hybrid.hybrid_encrypt(KEYS['ml_kem']['public_key'], message)
    ct_kyber = kem['aes']['ciphertext']
    time_kyber = kem['total_time']
    results.append({
        'algorithm': 'ML-KEM-768',
        'time': time_kyber,
        'size': len(ct_kyber),
        'security': '192 bits'
    })
    save_test_result('encryption', 'ML-KEM-768', message, time_kyber, len(ct_kyber), encrypted_data=ct_kyber)

    # Hybrid
    results.append({
        'algorithm': 'Hybrid (RSA+Kyber)',
        'time': time_rsa + time_kyber,
        'size': len(ct_rsa) + len(ct_kyber),
        'security': '>=192 bits'
    })
    save_test_result('encryption', 'Hybrid (RSA+Kyber)', message,
                     time_rsa + time_kyber, len(ct_rsa) + len(ct_kyber))

    return jsonify({'results': results})
