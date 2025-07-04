from flask import Blueprint, request, jsonify
from backend.routes.keys import KEYS
from backend.utils import classical, hybrid
from backend.database import save_test_result
import json
import tracemalloc

bp = Blueprint('encryption', __name__)
ENCRYPTED_RESULTS = {}

@bp.route('/encrypt', methods=['POST'])
def encrypt():
    data = request.json
    message = data.get("message", "")
    algorithm = data.get("algorithm", "")

    if not message:
        return jsonify({"error": "Message is empty"}), 400

    try:
        result = {}

        if algorithm == "rsa":
            tracemalloc.start()
            ciphertext, enc_time = classical.rsa_encrypt(KEYS['rsa'].publickey(), message)
            current, peak = tracemalloc.get_traced_memory()
            tracemalloc.stop()

            result = {
                'algorithm': "RSA-3072",
                'ciphertext': ciphertext,
                'encryption_time': enc_time,
                'ciphertext_size': len(ciphertext),
                'memory': peak
            }

        elif algorithm == "ml_kem_hybrid":
            tracemalloc.start()
            kem_result = hybrid.hybrid_encrypt(KEYS['ml_kem']['public_key'], message)
            current, peak = tracemalloc.get_traced_memory()
            tracemalloc.stop()

            aes = kem_result['aes']
            result = {
                'algorithm': "Hybrid (RSA+Kyber)",
                'encapsulated_key': kem_result['encapsulated_key'],
                'aes_ciphertext': aes['ciphertext'],
                'aes_tag': aes['tag'],
                'aes_nonce': aes['nonce'],
                'encryption_time': kem_result['total_time'],
                'ciphertext_size': len(aes['ciphertext']),
                'memory': peak
            }

        else:
            return jsonify({"error": "Unsupported algorithm"}), 400

        result_id = len(ENCRYPTED_RESULTS)
        ENCRYPTED_RESULTS[result_id] = {
            'algorithm': algorithm,
            'message': message,
            'result': result
        }
        result['result_id'] = result_id

        save_test_result('encryption', result['algorithm'], message,
                         result['encryption_time'], result['ciphertext_size'],
                         encrypted_data=json.dumps(result), success=True)

        return jsonify(result)

    except Exception as e:
        return jsonify({"error": f"Encryption failed: {str(e)}"}), 500

@bp.route('/decrypt', methods=['POST'])
def decrypt():
    data = request.json
    result_id = data.get("result_id")

    if result_id not in ENCRYPTED_RESULTS:
        return jsonify({"error": "Invalid result ID"}), 400

    try:
        record = ENCRYPTED_RESULTS[result_id]
        algo = record['algorithm']
        msg = record['message']
        res = record['result']

        if algo == "rsa":
            plaintext, dec_time = classical.rsa_decrypt(KEYS['rsa'], res['ciphertext'])
        elif algo == "ml_kem_hybrid":
            aes_data = {
                'ciphertext': res['aes_ciphertext'],
                'tag': res['aes_tag'],
                'nonce': res['aes_nonce']
            }
            plaintext, dec_time = hybrid.hybrid_decrypt(
                KEYS['ml_kem']['private_key'],
                int(res['encapsulated_key']),
                aes_data
            )
        else:
            return jsonify({"error": "Unsupported algorithm"}), 400

        save_test_result('decryption', res['algorithm'], plaintext,
                         dec_time, len(plaintext), success=(plaintext == msg))

        return jsonify({
            "algorithm": res['algorithm'],
            "plaintext": plaintext,
            "decryption_time": dec_time,
            "original_message": msg,
            "decryption_successful": (plaintext == msg)
        })

    except Exception as e:
        return jsonify({"error": f"Decryption failed: {str(e)}"}), 500

@bp.route('/get_encryption_results', methods=['GET'])
def get_encryption_results():
    return jsonify({
        'results': [
            {
                'id': rid,
                'algorithm': val['algorithm'],
                'message_preview': val['message'][:40] + '...' if len(val['message']) > 40 else val['message']
            }
            for rid, val in ENCRYPTED_RESULTS.items()
        ]
    })
