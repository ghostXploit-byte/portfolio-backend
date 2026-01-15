from flask import Flask, request, jsonify
from flask_cors import CORS
import sqlite3
import os

app = Flask(__name__)
CORS(app)

def init_db():
    conn = sqlite3.connect("messages.db")
    c = conn.cursor()
    c.execute("""
        CREATE TABLE IF NOT EXISTS messages (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            email TEXT,
            message TEXT
        )
    """)
    conn.commit()
    conn.close()

init_db()

@app.route("/", methods=["GET"])
def home():
    return "Backend running"

@app.route("/contact", methods=["POST"])
def contact():
    data = request.get_json()

    conn = sqlite3.connect("messages.db")
    c = conn.cursor()
    c.execute(
        "INSERT INTO messages (name, email, message) VALUES (?, ?, ?)",
        (data["name"], data["email"], data["message"])
    )
    conn.commit()
    conn.close()

    return jsonify({"message": "Message saved"})

@app.route("/messages", methods=["GET"])
def get_messages():
    conn = sqlite3.connect("messages.db")
    c = conn.cursor()
    c.execute("SELECT name, email, message FROM messages")
    rows = c.fetchall()
    conn.close()

    return jsonify(rows)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
