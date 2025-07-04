# backend/routes/verification.py

from flask import Blueprint, request, jsonify
from backend.routes.keys import KEYS
from backend.utils import classical, post_quantum
from backend.database import save_test_result

bp = Blueprint('verification', __name__)

@bp.route('/verify', methods=['POST'])
def verify():
    data = request.json
    message = data.get("message", "")
    sig_data = data.get("signature_data", {})
    algorithm = sig_data.get("algorithm", "")

    try:
        if "RSA" in algorithm:
            valid, verify_time = classical.rsa_verify(
                KEYS['rsa'].publickey(), message, sig_data['signature'])

        elif "ML-DSA" in algorithm and "Hybrid" not in algorithm:
            valid, verify_time = post_quantum.ml_dsa_verify(
                KEYS['ml_dsa']['public_key'], message, sig_data['signature'])

        elif "Hybrid" in algorithm:
            valid_rsa, t1 = classical.rsa_verify(
                KEYS['rsa'].publickey(), message, sig_data['rsa_signature'])
            valid_pq, t2 = post_quantum.ml_dsa_verify(
                KEYS['ml_dsa']['public_key'], message, sig_data['ml_dsa_signature'])
            valid = valid_rsa and valid_pq
            verify_time = t1 + t2

        else:
            return jsonify({"error": "Unsupported verification algorithm"}), 400

        save_test_result('verification', algorithm, message, verify_time, 0, success=valid)

        return jsonify({
            "valid": valid,
            "verification_time": verify_time,
            "algorithm": algorithm
        })

    except Exception as e:
        return jsonify({"error": f"Verification failed: {str(e)}"}), 500
