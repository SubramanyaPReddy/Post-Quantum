# backend/database.py

import sqlite3
import json
from backend.config import DATABASE_FILE

def init_database():
    conn = sqlite3.connect(DATABASE_FILE)
    cursor = conn.cursor()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS test_results (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
            operation_type TEXT NOT NULL,
            algorithm_name TEXT NOT NULL,
            message_text TEXT NOT NULL,
            execution_time REAL NOT NULL,
            data_size INTEGER NOT NULL,
            encrypted_data TEXT,
            signature_data TEXT,
            success BOOLEAN NOT NULL,
            additional_info TEXT
        )
    ''')

    cursor.execute('CREATE INDEX IF NOT EXISTS idx_timestamp ON test_results(timestamp)')
    cursor.execute('CREATE INDEX IF NOT EXISTS idx_algorithm ON test_results(algorithm_name)')

    conn.commit()
    conn.close()

def save_test_result(operation_type, algorithm_name, message_text, execution_time, 
                     data_size, encrypted_data=None, signature_data=None, 
                     success=True, additional_info=None):
    conn = sqlite3.connect(DATABASE_FILE)
    cursor = conn.cursor()

    cursor.execute('''
        INSERT INTO test_results 
        (operation_type, algorithm_name, message_text, execution_time, data_size, 
         encrypted_data, signature_data, success, additional_info)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', (
        operation_type, algorithm_name, message_text, execution_time, data_size,
        encrypted_data, signature_data, success,
        json.dumps(additional_info) if additional_info else None
    ))

    conn.commit()
    result_id = cursor.lastrowid
    conn.close()
    return result_id
