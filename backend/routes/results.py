from flask import Blueprint, jsonify
import sqlite3
from backend.config import DATABASE_FILE

bp = Blueprint('results', __name__)

@bp.route('/get_test_history', methods=['GET'])
def get_test_history():
    try:
        conn = sqlite3.connect(DATABASE_FILE)
        cursor = conn.cursor()
        cursor.execute('''
            SELECT timestamp, operation_type, algorithm_name, execution_time, data_size, success
            FROM test_results
            ORDER BY timestamp DESC
            LIMIT 50
        ''')
        rows = cursor.fetchall()
        conn.close()

        history = [{
            'timestamp': r[0],
            'operation': r[1],
            'algorithm': r[2],
            'time': r[3],
            'size': r[4],
            'success': bool(r[5])
        } for r in rows]

        return jsonify({'history': history})
    except Exception as e:
        return jsonify({'error': f"Failed to get history: {str(e)}"}), 500

@bp.route('/evaluate_live', methods=['GET'])
def evaluate_live():
    try:
        conn = sqlite3.connect(DATABASE_FILE)
        cursor = conn.cursor()
        cursor.execute('''
            SELECT algorithm_name, AVG(execution_time), AVG(data_size), COUNT(*)
            FROM test_results
            GROUP BY algorithm_name
        ''')
        rows = cursor.fetchall()
        conn.close()

        results = [{
            'algorithm': r[0],
            'avg_time (s)': round(r[1], 4),
            'avg_data_size (bytes)': int(r[2]),
            'test_count': r[3]
        } for r in rows]

        return jsonify({'evaluations': results})
    except Exception as e:
        return jsonify({'error': f"Evaluation failed: {str(e)}"}), 500
