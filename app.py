"""API REST de tarefas com login (Flask + SQLite)."""
import os
import sqlite3
from functools import wraps

from flask import Flask, g, jsonify, request, send_from_directory, session
from werkzeug.security import check_password_hash, generate_password_hash

app = Flask(__name__, static_folder="static")
app.secret_key = os.environ.get("SECRET_KEY", "dev-only-change-me")
DB = "todo.db"


def db():
    if "db" not in g:
        g.db = sqlite3.connect(DB)
        g.db.row_factory = sqlite3.Row
    return g.db


@app.teardown_appcontext
def close_db(_):
    if "db" in g:
        g.db.close()


def init_db():
    with sqlite3.connect(DB) as con:
        con.executescript("""
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY, username TEXT UNIQUE NOT NULL, password TEXT NOT NULL);
            CREATE TABLE IF NOT EXISTS tasks (
                id INTEGER PRIMARY KEY, user_id INTEGER NOT NULL REFERENCES users(id),
                title TEXT NOT NULL, done INTEGER NOT NULL DEFAULT 0);
        """)


def login_required(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        if "user_id" not in session:
            return jsonify(error="não autenticado"), 401
        return f(*args, **kwargs)
    return wrapper


@app.get("/")
def index():
    return send_from_directory("static", "index.html")


@app.post("/api/register")
def register():
    data = request.get_json() or {}
    user, pwd = data.get("username", "").strip(), data.get("password", "")
    if len(user) < 3 or len(pwd) < 6:
        return jsonify(error="usuário (3+) e senha (6+) obrigatórios"), 400
    try:
        db().execute("INSERT INTO users (username, password) VALUES (?, ?)", (user, generate_password_hash(pwd)))
        db().commit()
    except sqlite3.IntegrityError:
        return jsonify(error="usuário já existe"), 409
    return jsonify(ok=True), 201


@app.post("/api/login")
def login():
    data = request.get_json() or {}
    row = db().execute("SELECT * FROM users WHERE username = ?", (data.get("username"),)).fetchone()
    if not row or not check_password_hash(row["password"], data.get("password", "")):
        return jsonify(error="credenciais inválidas"), 401
    session["user_id"], session["username"] = row["id"], row["username"]
    return jsonify(username=row["username"])


@app.post("/api/logout")
def logout():
    session.clear()
    return jsonify(ok=True)


@app.get("/api/me")
def me():
    return jsonify(username=session.get("username"))


@app.get("/api/tasks")
@login_required
def list_tasks():
    rows = db().execute("SELECT id, title, done FROM tasks WHERE user_id = ? ORDER BY id DESC",
                        (session["user_id"],)).fetchall()
    return jsonify([dict(r) for r in rows])


@app.post("/api/tasks")
@login_required
def create_task():
    title = (request.get_json() or {}).get("title", "").strip()
    if not title:
        return jsonify(error="título obrigatório"), 400
    cur = db().execute("INSERT INTO tasks (user_id, title) VALUES (?, ?)", (session["user_id"], title))
    db().commit()
    return jsonify(id=cur.lastrowid, title=title, done=0), 201


@app.patch("/api/tasks/<int:task_id>")
@login_required
def toggle_task(task_id):
    db().execute("UPDATE tasks SET done = 1 - done WHERE id = ? AND user_id = ?", (task_id, session["user_id"]))
    db().commit()
    return jsonify(ok=True)


@app.delete("/api/tasks/<int:task_id>")
@login_required
def delete_task(task_id):
    db().execute("DELETE FROM tasks WHERE id = ? AND user_id = ?", (task_id, session["user_id"]))
    db().commit()
    return jsonify(ok=True)


if __name__ == "__main__":
    init_db()
    app.run(debug=True)
