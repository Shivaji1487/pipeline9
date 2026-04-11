from flask import Flask, render_template, request, redirect, url_for
import mysql.connector
import os
import time

app = Flask(__name__)

# Database Connection Helper with Retries
# In a cluster, the DB might take a few seconds to start; retries prevent crashes.
def get_db_connection():
    attempts = 0
    while attempts < 5:
        try:
            conn = mysql.connector.connect(
                host=os.getenv("DB_HOST", "mysql-service"),
                user=os.getenv("DB_USER", "root"),
                password=os.getenv("DB_PASSWORD", "admin123"),
                database="abc_bank"
            )
            return conn
        except mysql.connector.Error as err:
            attempts += 1
            print(f"Attempt {attempts}: Database connection failed. Retrying...")
            time.sleep(2)
    return None

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        pw = request.form.get('password')
        
        conn = get_db_connection()
        if conn:
            cursor = conn.cursor(dictionary=True)
            # Security Note: Using parameterized queries to prevent SQL Injection
            query = "SELECT * FROM users WHERE username=%s AND password=%s"
            cursor.execute(query, (username, pw))
            user = cursor.fetchone()
            
            cursor.close()
            conn.close()

            if user:
                return f"<h2>Login Successful! Welcome, {username}.</h2> <a href='/'>Go Home</a>"
            else:
                return "<h2>Invalid Credentials!</h2> <a href='/login'>Try Again</a>"
        else:
            return "<h2>Database Connection Error!</h2>"
            
    return render_template('login.html')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        name = request.form.get('username')
        email = request.form.get('email')
        pw = request.form.get('password')
        
        conn = get_db_connection()
        if conn:
            try:
                cursor = conn.cursor()
                query = "INSERT INTO users (username, email, password) VALUES (%s, %s, %s)"
                cursor.execute(query, (name, email, pw))
                conn.commit()
                cursor.close()
                conn.close()
                return "<h2>Registration Successful!</h2> <a href='/login'>Now Login Here</a>"
            except mysql.connector.Error as err:
                return f"<h2>Error: {err}</h2>"
        else:
            return "<h2>Database Connection Error!</h2>"
            
    return render_template('signup.html')

if __name__ == '__main__':
    # host='0.0.0.0' allows access from outside the container
    # port=5000 is the standard Flask port
    app.run(host='0.0.0.0', port=5000)