# backend/app.py

from flask import Flask, jsonify
from flask_cors import CORS
import os

from backend.database import init_database
from backend.config import NIST_ALGORITHMS

# Import route blueprints
from backend.routes.keys import bp as keys_bp
from backend.routes.results import bp as results_bp
from backend.routes.verification import bp as verification_bp
from backend.routes.multiencrypt import bp as multiencrypt_bp
from backend.routes.multisign import bp as multisign_bp

app = Flask(__name__)
CORS(app)

# Register all API route blueprints
app.register_blueprint(keys_bp)
app.register_blueprint(results_bp)
app.register_blueprint(verification_bp)
app.register_blueprint(multiencrypt_bp)
app.register_blueprint(multisign_bp)

# Health check root route for Render
@app.route("/", methods=["GET"])
def index():
    return jsonify({"message": "✅ Post-Quantum Crypto Backend is running!"})

# Detailed health endpoint
@app.route("/health", methods=["GET"])
def health():
    return jsonify({
        "status": "healthy",
        "database": "connected",
        "nist_standards": NIST_ALGORITHMS
    })

if __name__ == '__main__':
    init_database()
    print("🔐 Flask NIST Crypto Backend Running on 0.0.0.0:", os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 5000)))
