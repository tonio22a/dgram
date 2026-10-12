from flask import Flask, render_template, request, redirect, session
import sqlite3
from datetime import datetime

def init_db():
    conn = sqlite3.connect("users.db")
    conn.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            email TEXT UNIQUE,
            password TEXT
        )
    """)
    conn.execute("""
        CREATE TABLE IF NOT EXISTS messages (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            text TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    conn.commit()
    conn.close()

def initms_db():
    conn = sqlite3.connect("messages.db")
    conn.execute("""
        CREATE TABLE IF NOT EXISTS messages (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            author TEXT,
            text TEXT,
            created_at TIMESTAMP
        )
    """)
    conn.commit()
    conn.close()

init_db()
initms_db()

app = Flask(__name__)
app.secret_key = "dgram-secret-key456"

@app.route("/")
def home():
    if "user_id" not in session:
        return render_template("welcome.html")
    
    conn = sqlite3.connect("users.db")
    user = conn.execute(
        "SELECT name, email, password FROM users WHERE id = ?",
        (session["user_id"],)
    ).fetchone()
    conn.close()
    
    print(user)  # ("Ваня", "van@mail.ru", "12345")
    
    now = datetime.now().strftime("%d/%b/%Y")
    tags = session.get("user_name", "Гость")
    return render_template("home.html", time=now, name=tags, user=user)

@app.route("/account", methods=["GET", "POST"])
def account():
    if "user_id" not in session:
        return render_template("welcome.html")
    conn = sqlite3.connect("users.db")
    if request.method == "POST":
        name = request.form["name"]
        email = request.form["email"]
        password = request.form["password"]
        
        user = conn.execute(
            "UPDATE users SET name = ?, email = ?, password = ? WHERE id = ?",
            (name, email, password, session["user_id"])
        )
        session["user_name"] = name
        conn.commit()
        return redirect("/")
    user = conn.execute(
        "SELECT name, email, password FROM users WHERE id = ?",
        (session["user_id"],)
    ).fetchone()

    conn.close()
    
    return render_template("account.html", user=user)


@app.route("/wall", methods=["GET", "POST"])
def wall():
    if "user_id" not in session:
        return redirect("/login")
    
    if request.method == "POST":
        text = request.form["text"]
        if text:
            conn = sqlite3.connect("users.db")
            conn.execute(
                "INSERT INTO messages (user_id, text) VALUES (?, ?)",
                (session["user_id"], text)
            )
            conn.commit()
            conn.close()
        return redirect("/wall")
    
    conn = sqlite3.connect("users.db")
    rows = conn.execute("""
        SELECT users.name, messages.text, messages.created_at
        FROM messages
        JOIN users ON messages.user_id = users.id
        ORDER BY messages.created_at DESC
    """).fetchall()
    conn.close()
    
    return render_template("wall.html", messages=rows)


@app.route("/faq")
def faq():
    return render_template("faq.html")

@app.route("/welcome")
def welcome():
    return render_template("welcome.html")

@app.route("/friends")
def friends():
    return render_template("friends.html")

@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")

@app.route("/contact")
def contact():
    return render_template("contact.html")

@app.route("/politic")
def politic():
    return render_template("politic.html")

@app.route("/invites")
def invites():
    return render_template("invites.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]
        
        conn = sqlite3.connect("users.db")
        user = conn.execute(
            "SELECT id, name FROM users WHERE email = ? AND password = ?",
            (email, password)
        ).fetchone()
        conn.close()

        if user:                             
            session["user_id"] = user[0]        
            session["user_name"] = user[1]         
            return redirect("/")                    
        else:
            return "Неверный email или пароль" 
        
    return render_template("login.html")

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        name = request.form["name"]
        email = request.form["email"]
        password = request.form["password"]
        tag = request.form["tag"]
        
        conn = sqlite3.connect("users.db")
        conn.execute(
                "INSERT INTO users (name, email, password, tag) VALUES (?, ?, ?, ?)",
                (name, email, password, tag)
            )
        conn.commit()
        conn.close()
        return redirect("/login")
    
    return render_template("register.html")

if __name__ == "__main__":
    app.run(debug=True)