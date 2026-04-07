from flask import Flask, render_template, request
import mysql.connector
import os

app = Flask(__name__)

# Database Connection
def get_db_connection():
    return mysql.connector.connect(
        host=os.getenv("DB_HOST", "mysql-service"),
        user=os.getenv("DB_USER", "root"),
        password=os.getenv("DB_PASSWORD", "admin123"),
        database="abc_bank"
    )

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        name = request.form.get('username')
        email = request.form.get('email')
        pw = request.form.get('password')
        
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO users (username, email, password) VALUES (%s, %s, %s)", (name, email, pw))
        conn.commit()
        cursor.close()
        conn.close()
        return "Registration Successful! <a href='/'>Go Back</a>"
    return render_template('signup.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)