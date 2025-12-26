from flask import Flask, jsonify
import psycopg2
import os

app = Flask(__name__)

def get_db_connection():
    return psycopg2.connect(
        host=os.environ.get("DB_HOST"),
        database=os.environ.get("DB_NAME"),
        user=os.environ.get("DB_USER"),
        password=os.environ.get("DB_PASSWORD"),
    )

@app.route("/")
def home():
    return "Backend is running"

@app.route("/health")
def health():
    try:
        conn = get_db_connection()
        conn.close()
        return "DB connection OK", 200
    except Exception as e:
        return str(e), 500

@app.route("/items")
def get_items():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT id, name FROM items;")
    rows = cur.fetchall()
    cur.close()
    conn.close()

    items = []
    for row in rows:
        items.append({
            "id": row[0],
            "name": row[1]
        })

    return jsonify(items)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
