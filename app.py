from dotenv import load_dotenv
load_dotenv()

from flask import Flask, jsonify, request
import os
import pymysql
from datetime import datetime
from flask_cors import CORS

app = Flask(__name__)
CORS(app) # Enable CORS for all origins and all routes. For production, restrict origins.

# --- Database Configuration: Retrieve values from environment variables ---
# These default values are for local development/testing and should be overridden in production.
DB_HOST = os.environ.get('DB_HOST', 'localhost')
DB_NAME = os.environ.get('DB_NAME', 'mydatabase')
DB_USER = os.environ.get('DB_USER', 'myuser')
DB_PASS = os.environ.get('DB_PASS', 'mypassword')

def get_db_connection():
    """Establishes and returns a database connection."""
    try:
        conn = pymysql.connect(host=DB_HOST, database=DB_NAME, user=DB_USER, password=DB_PASS)
        return conn
    except Exception as e:
        print(f"Database connection failed: {e}")
        return None

@app.route('/api/data', methods=['GET'])
def get_data():
    """
    API endpoint to read the latest message from the database.
    """
    conn = get_db_connection()
    if conn is None:
        return jsonify({"message": "Database connection error", "timestamp": datetime.now().isoformat()}), 500

    try:
        cursor = conn.cursor()
        cursor.execute("SELECT message, timestamp FROM messages ORDER BY timestamp DESC LIMIT 1;")
        result = cursor.fetchone()

        if result:
            message, timestamp = result
            return jsonify({"message": message, "timestamp": timestamp.isoformat()})
        else:
            return jsonify({"message": "No data in database yet.", "timestamp": datetime.now().isoformat()})

    except Exception as e:
        print(f"Error during database read operation: {e}")
        return jsonify({"message": f"Error reading data: {e}", "timestamp": datetime.now().isoformat()}), 500
    finally:
        if conn:
            cursor.close()
            conn.close()

@app.route('/api/add-message', methods=['POST'])
def add_message():
    """
    API endpoint to add a new message to the database.
    """
    conn = get_db_connection()
    if conn is None:
        return jsonify({"message": "Database connection error", "timestamp": datetime.now().isoformat()}), 500

    try:
        data = request.get_json()
        message = data.get('message')

        if not message:
            return jsonify({"message": "Message content is required"}), 400

        cursor = conn.cursor()
        current_time = datetime.now()
        cursor.execute("INSERT INTO messages (message, timestamp) VALUES (%s, %s);", (message, current_time))
        conn.commit()

        return jsonify({"message": "Message added successfully", "timestamp": current_time.isoformat()}), 201

    except Exception as e:
        conn.rollback()
        print(f"Error during database write operation: {e}")
        return jsonify({"message": f"Error adding message: {e}", "timestamp": datetime.now().isoformat()}), 500
    finally:
        if conn:
            cursor.close()
            conn.close()

@app.route('/')
def health_check():
    """Basic health check endpoint."""
    return "Backend is running!"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001)

    