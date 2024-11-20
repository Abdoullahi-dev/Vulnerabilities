import os
import sys
import sqlite3
import hashlib

from flask import Flask, render_template, send_from_directory
from flask import request, jsonify, abort, redirect


app = Flask(__name__)

def connect_db() -> None:
    conn = sqlite3.connect("webapp.db")
    c = conn.cursor()
    c.execute("""
    CREATE TABLE IF NOT EXISTS users (
        userID TEXT PRIMARY KEY NOT NULL UNIQUE,
        username TEXT NOT NULL,
        password TEXT NOT NULL,
        admin INT DEFAULT 0 CHECK (admin IN (0, 1))
    )
    """)

    conn.commit()
    conn.close()

def get_db():
    conn = sqlite3.connect("webapp.db")
    conn.row_factory = sqlite3.Row
    return conn

@app.route("/")
def index():
    return render_template("index.html")


@app.route("/login", methods=["POST"])
def login():
    username = request.form.get("username")
    password = request.form.get("password")

    hashed_password = hashlib.md5(password.encode()).hexdigest()

    db = get_db()
    user = db.execute('SELECT * FROM users WHERE username = ? AND password = ?',
                     (username, hashed_password)).fetchone()
    db.close()
    
    if user:
        return redirect('/admin')

    return jsonify({
        "error": "Invalid [username, password] credentials provided.",
        "status": 401
    }), 401


@app.route("/admin")
def admin():
    db = get_db()
    users = db.execute("SELECT * FROM users;").fetchall()
    db.close()

    return render_template("admin.html", users=users)


@app.route("/assets")
def list_dir():
    base_dir = os.path.abspath(os.path.dirname(__file__))
    files = []

    for item in os.listdir(base_dir):
        item_path = os.path.join(base_dir, item)
        item_type = 'Directory' if os.path.isdir(item_path) else 'File'
        files.append({
            'name': item,
            'type': item_type
        })

    html = '<h1>Directory Listing</h1><ul>'
    for file in files:
        html += f'<li><a href="/assets/{file["name"]}">{file["name"]}</a> ({file["type"]})</li>'
    html += '</ul>'
    
    return html


@app.route('/assets/<path:filename>')
def serve_file(filename):
    base_dir = os.path.abspath(os.path.dirname(__file__))
    return send_from_directory(base_dir, filename)

if __name__ == "__main__":
    connect_db()
    app.run(debug=True)
