import sqlite3
from werkzeug.security import generate_password_hash, check_password_hash
from init_db import DB_NAME

def add_user(username, password, role="user"):
    """Register a new user with hashed password."""
    hashed_password = generate_password_hash(password)

    try:
        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()
        cursor.execute("INSERT INTO users (username, password, role) VALUES (?, ?, ?)", 
                       (username, hashed_password, role))
        conn.commit()
        return {"success": True, "message": "✅ User registered successfully!"}

    except sqlite3.IntegrityError:
        return {"success": False, "message": "⚠️ Username already exists!"}

    finally:
        conn.close()

def verify_user(username, password):
    """Verify user credentials."""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    
    cursor.execute("SELECT * FROM users WHERE username=?", (username,))
    user = cursor.fetchone()
    
    conn.close()

    if user and check_password_hash(user[2], password):  
        return {"success": True, "message": "✅ Login successful!", "user_id": user[0]}
    
    return {"success": False, "message": "❌ Invalid username or password!"}

if __name__ == "__main__":
    print(add_user("testuser", "password123"))  # Example signup
    print(verify_user("testuser", "password123"))  # Example login
