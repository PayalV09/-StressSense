import sqlite3
import logging

# Database Name
DB_NAME = "data_collection.db"

# Configure Logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")


def create_table():
    """Ensure the database table exists before inserting data."""
    try:
        with sqlite3.connect(DB_NAME) as conn:
            cursor = conn.cursor()
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS stress_data (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id INTEGER NOT NULL,
                    stress_level INTEGER NOT NULL CHECK(stress_level BETWEEN 1 AND 10),
                    sleep_hours REAL NOT NULL CHECK(sleep_hours >= 0),
                    diet_score INTEGER NOT NULL CHECK(diet_score BETWEEN 1 AND 10),
                    exercise_minutes INTEGER NOT NULL CHECK(exercise_minutes >= 0),
                    mood TEXT NOT NULL
                )
            """)
            conn.commit()
            logging.info("✅ Database table ensured.")
    except sqlite3.Error as e:
        logging.error(f"⚠️ Table creation error: {e}")


def collect_data(user_id, stress_level, sleep_hours, diet_score, exercise_minutes, mood):
    """Insert stress data into the database."""
    try:
        with sqlite3.connect(DB_NAME) as conn:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO stress_data (user_id, stress_level, sleep_hours, diet_score, exercise_minutes, mood)
                VALUES (?, ?, ?, ?, ?, ?)
            """, (user_id, stress_level, sleep_hours, diet_score, exercise_minutes, mood))
            conn.commit()
            logging.info("✅ Stress data recorded successfully.")
            return {"success": True, "message": "✅ Stress data recorded!"}
    except sqlite3.Error as e:
        logging.error(f"⚠️ Database error: {e}")
        return {"success": False, "message": f"⚠️ Database error: {e}"}


def fetch_all_data():
    """Retrieve all stress records."""
    try:
        with sqlite3.connect(DB_NAME) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM stress_data")
            rows = cursor.fetchall()
            return rows
    except sqlite3.Error as e:
        logging.error(f"⚠️ Database fetch error: {e}")
        return []


if __name__ == "__main__":
    create_table()  # Ensure the table exists
    print(collect_data(1, 6, 7.5, 8, 30, "Happy"))  # Example data entry
    print(fetch_all_data())  # Fetch and display stored records
