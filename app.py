from flask import Flask, render_template, request, redirect, url_for
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

# FIXED: Added POST method and database verification logic
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        # Check if user exists with matching password
        query = "SELECT * FROM users WHERE username = %s AND password = %s"
        cursor.execute(query, (username, password))
        user = cursor.fetchone()
        
        cursor.close()
        conn.close()

        if user:
            return f"Welcome {username}! Login Successful. <a href='/'>Go Back</a>"
        else:
            return "Invalid Credentials! <a href='/login'>Try Again</a>"
            
    return render_template('login.html')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        name = request.form.get('username')
        email = request.form.get('email')
        pw = request.form.get('password')
        
        conn = get_db_connection()
        cursor = conn.cursor()
        try:
            cursor.execute("INSERT INTO users (username, email, password) VALUES (%s, %s, %s)", (name, email, pw))
            conn.commit()
            return "Registration Successful! <a href='/login'>Login Now</a>"
        except mysql.connector.Error as err:
            return f"Error: {err} <a href='/signup'>Try Again</a>"
        finally:
            cursor.close()
            conn.close()
            
    return render_template('signup.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)