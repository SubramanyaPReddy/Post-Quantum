from flask import Blueprint, request, jsonify
from backend.routes.keys import KEYS
from backend.utils import classical, post_quantum
from backend.database import save_test_result
import json
import tracemalloc

bp = Blueprint('signing', __name__)

@bp.route('/sign', methods=['POST'])
def sign():
    data = request.json
    message = data.get("message", "")
    algorithm = data.get("algorithm", "")

    if not message:
        return jsonify({"error": "Message is empty"}), 400

    try:
        result = {}

        if algorithm == "rsa":
            signature, sig_time = classical.rsa_sign(KEYS['rsa'], message)
            result = {
                'algorithm': "RSA-3072",
                'signature': signature,
                'signing_time': sig_time,
                'signature_size': len(signature)
            }

        elif algorithm == "ml_dsa":
            res = post_quantum.ml_dsa_sign(KEYS['ml_dsa']['private_key'], message)
            result = {
                'algorithm': "ML-DSA-65",
                'signature': res['signature'],
                'signing_time': res['time'],
                'signature_size': res['size']
            }

        elif algorithm == "hybrid":
            rsa_sig, t1 = classical.rsa_sign(KEYS['rsa'], message)
            pq_sig = post_quantum.ml_dsa_sign(KEYS['ml_dsa']['private_key'], message)
            result = {
                'algorithm': "Hybrid (RSA+Dilithium)",
                'rsa_signature': rsa_sig,
                'ml_dsa_signature': pq_sig['signature'],
                'signing_time': t1 + pq_sig['time'],
                'signature_size': len(rsa_sig) + pq_sig['size']
            }

        else:
            return jsonify({"error": "Unsupported signing algorithm"}), 400

        save_test_result('signing', result['algorithm'], message,
                         result['signing_time'], result['signature_size'],
                         signature_data=json.dumps(result), success=True)

        return jsonify(result)

    except Exception as e:
        return jsonify({"error": f"Signing failed: {str(e)}"}), 500
