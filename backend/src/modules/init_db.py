import sqlite3

DB_NAME = "stress.db"

def init_db():
    """Initialize the database and create tables."""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    # User Table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT, 
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            role TEXT DEFAULT 'user'
        )
    """)

    # Stress Data Table (User Stress Levels)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS stress_data (
            id INTEGER PRIMARY KEY AUTOINCREMENT, 
            user_id INTEGER,
            stress_level INTEGER,
            sleep_hours REAL,
            diet_score INTEGER,
            exercise_minutes INTEGER,
            mood TEXT,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY(user_id) REFERENCES users(id)
        )
    """)

    conn.commit()
    conn.close()
    print("✅ Database initialized successfully!")

if __name__ == "__main__":
    init_db()
