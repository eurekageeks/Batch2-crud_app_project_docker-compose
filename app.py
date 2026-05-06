from flask import Flask, request, jsonify
from flask_cors import CORS
import mysql.connector
import time

app = Flask(__name__)
CORS(app)

# ✅ Retry DB connection
def get_db():
    while True:
        try:
            conn = mysql.connector.connect(
                host="db",
                user="root",
                password="root",
                database="test_db"
            )
            print("✅ Connected to MySQL")
            return conn
        except Exception as e:
            print("⏳ Waiting for MySQL...", e)
            time.sleep(3)

# ✅ Create table safely
conn = get_db()
cursor = conn.cursor()
cursor.execute("""
CREATE TABLE IF NOT EXISTS users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255)
)
""")
conn.commit()
conn.close()

# 🔹 GET ALL
@app.route('/users', methods=['GET'])
def get_users():
    try:
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users")
        data = cursor.fetchall()
        conn.close()
        return jsonify(data)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# 🔹 CREATE
@app.route('/users', methods=['POST'])
def create_user():
    try:
        data = request.json
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO users (name) VALUES (%s)", (data['name'],))
        conn.commit()
        conn.close()
        return jsonify({"msg": "created"})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# 🔹 UPDATE
@app.route('/users/<int:id>', methods=['PUT'])
def update_user(id):
    try:
        data = request.json
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute("UPDATE users SET name=%s WHERE id=%s", (data['name'], id))
        conn.commit()
        conn.close()
        return jsonify({"msg": "updated"})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# 🔹 DELETE
@app.route('/users/<int:id>', methods=['DELETE'])
def delete_user(id):
    try:
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM users WHERE id=%s", (id,))
        conn.commit()
        conn.close()
        return jsonify({"msg": "deleted"})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)