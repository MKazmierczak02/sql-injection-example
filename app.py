from flask import Flask, request, render_template
import sqlite3

app = Flask(__name__)

# Utworzenie przykładowej bazy danych
def init_db():
    conn = sqlite3.connect("example.db")
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT,
            password TEXT
        )
    """)
    cursor.execute("INSERT INTO users (username, password) VALUES ('admin', 'admin')")
    cursor.execute("INSERT INTO users (username, password) VALUES ('user', 'password')")
    conn.commit()
    conn.close()

init_db()

# Strona główna
@app.route('/', methods=['GET', 'POST'])
def home():
    vulnerable_response = ""
    secure_response = ""

    if request.method == 'POST':
        username = request.form.get('username', '')
        password = request.form.get('password', '')
        form_type = request.form.get('form_type', '')

        if form_type == "vulnerable":
            # Obsługa podatnego formularza
            conn = sqlite3.connect("example.db")
            cursor = conn.cursor()
            query = f"SELECT * FROM users WHERE username = '{username}' AND password = '{password}'"
            cursor.execute(query)
            user = cursor.fetchone()
            conn.close()

            if user:
                vulnerable_response = f"Welcome, {username}!"
            else:
                vulnerable_response = "Invalid credentials"

        elif form_type == "secure":
            # Obsługa zabezpieczonego formularza
            conn = sqlite3.connect("example.db")
            cursor = conn.cursor()
            query = "SELECT * FROM users WHERE username = ? AND password = ?"
            cursor.execute(query, (username, password))
            user = cursor.fetchone()
            conn.close()

            if user:
                secure_response = f"Welcome, {username}!"
            else:
                secure_response = "Invalid credentials"

    return render_template(
        "index.html",
        vulnerable_response=vulnerable_response,
        secure_response=secure_response
    )

if __name__ == '__main__':
    app.run(debug=True)
