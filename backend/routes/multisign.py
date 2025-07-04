from flask import Blueprint, request, jsonify
from backend.routes.keys import KEYS
from backend.utils import classical, post_quantum
from backend.database import save_test_result

bp = Blueprint('multisign', __name__)

@bp.route('/sign_all', methods=['POST'])
def sign_all():
    data = request.json
    message = data.get("message", "")
    if not message:
        return jsonify({"error": "Message is empty"}), 400

    results = []

    # RSA
    sig_rsa, time_rsa = classical.rsa_sign(KEYS['rsa'], message)
    results.append({
        'algorithm': 'RSA-3072',
        'time': time_rsa,
        'size': len(sig_rsa),
        'security': '128 bits'
    })
    save_test_result('signing', 'RSA-3072', message, time_rsa, len(sig_rsa), signature_data=sig_rsa)

    # Dilithium
    pq = post_quantum.ml_dsa_sign(KEYS['ml_dsa']['private_key'], message)
    results.append({
        'algorithm': 'ML-DSA-65',
        'time': pq['time'],
        'size': pq['size'],
        'security': '192 bits'
    })
    save_test_result('signing', 'ML-DSA-65', message, pq['time'], pq['size'], signature_data=pq['signature'])

    # Hybrid
    results.append({
        'algorithm': 'Hybrid (RSA+Dilithium)',
        'time': time_rsa + pq['time'],
        'size': len(sig_rsa) + pq['size'],
        'security': '>=192 bits'
    })
    save_test_result('signing', 'Hybrid (RSA+Dilithium)', message,
                     time_rsa + pq['time'], len(sig_rsa) + pq['size'])

    return jsonify({'results': results})
