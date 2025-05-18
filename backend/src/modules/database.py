import os
import sqlite3
from werkzeug.security import generate_password_hash, check_password_hash

DB_NAME = "stress.db"

def init_db():
    """Initialize the database and create tables."""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT, 
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            role TEXT DEFAULT 'user'  -- 'user' or 'admin'
        )
    """)
    
    conn.commit()
    conn.close()
    print("✅ Database initialized successfully!")

def add_user(username, password, role="user"):
    """Add a new user with hashed password."""
    hashed_password = generate_password_hash(password)
    
    try:
        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()
        
        cursor.execute("INSERT INTO users (username, password, role) VALUES (?, ?, ?)", 
                       (username, hashed_password, role))
        conn.commit()
        return {"success": True, "message": "User registered successfully!"}
    
    except sqlite3.IntegrityError:
        return {"success": False, "message": "⚠️ Username already exists!"}
    
    finally:
        conn.close()

def get_user(username):
    """Retrieve user details by username."""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    
    cursor.execute("SELECT * FROM users WHERE username=?", (username,))
    user = cursor.fetchone()
    
    conn.close()
    return user

def verify_user(username, password):
    """Verify user credentials."""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    
    cursor.execute("SELECT * FROM users WHERE username=?", (username,))
    user = cursor.fetchone()
    
    conn.close()

    if user and check_password_hash(user[2], password):  # user[2] is hashed password
        return {"success": True, "message": "✅ Login successful!", "role": user[3]}
    
    return {"success": False, "message": "❌ Invalid username or password!"}

if __name__ == "__main__":
    init_db()  # Run this script to create the database
