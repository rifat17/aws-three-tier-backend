from flask import Flask, jsonify, request
import os
import pymysql
from datetime import datetime
from flask_cors import CORS
from dotenv import load_dotenv

load_dotenv()
app = Flask(__name__)
CORS(app)

DB_HOST = os.environ.get('DB_HOST', 'localhost')
DB_NAME = os.environ.get('DB_NAME', 'mydatabase')
DB_USER = os.environ.get('DB_USER', 'appuser')
DB_PASS = os.environ.get('DB_PASS', 'password')
PORT = int(os.environ.get('PORT', 5000))

def get_db_connection():
    return pymysql.connect(host=DB_HOST, database=DB_NAME, user=DB_USER, password=DB_PASS)

@app.route('/api/data')
def get_data():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT message, timestamp FROM messages ORDER BY timestamp DESC LIMIT 1")
    result = cursor.fetchone()
    conn.close()
    
    if result:
        return jsonify({"message": result[0], "timestamp": result[1].isoformat()})
    return jsonify({"message": "No messages yet"})

@app.route('/api/add-message', methods=['POST'])
def add_message():
    data = request.get_json()
    message = data['message']
    
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO messages (message, timestamp) VALUES (%s, %s)", 
                   (message, datetime.now()))
    conn.commit()
    conn.close()
    
    return jsonify({"message": "Message added!"})

@app.route('/')
def home():
    return "AWS Backend is running!"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=PORT)

    