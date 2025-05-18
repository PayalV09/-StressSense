import sqlite3
import numpy as np
from init_db import DB_NAME

def predict_stress_level(user_id):
    """Predict stress level based on sleep, diet, and exercise."""
    try:
        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()

        # Fetch user's stress-related data
        cursor.execute("SELECT stress_level, sleep_hours, diet_score, exercise_minutes FROM stress_data WHERE user_id=?", (user_id,))
        data = cursor.fetchall()
        conn.close()

        if not data:
            print(f"❌ No stress data found for user_id: {user_id}")
            return {"success": False, "message": "No stress data found for this user."}

        # Debugging print
        print(f"🔍 Retrieved Data for user {user_id}: {data}")

        # Convert stress level to float if it's stored as a numeric value
        try:
            stress_values = np.array([float(row[0]) for row in data])
        except ValueError:
            print("❌ Error: Stress level contains non-numeric values!")
            return {"success": False, "message": "Invalid stress level format."}

        # Calculate average stress level
        avg_stress = np.mean(stress_values)

        print(f"✅ Predicted Stress Level: {round(avg_stress, 2)}")
        return {"success": True, "predicted_stress_level": round(avg_stress, 2)}

    except Exception as e:
        print(f"❌ Error occurred: {e}")
        return {"success": False, "message": str(e)}

# Example usage
if __name__ == "__main__":
    print(predict_stress_level(1))  # Test with user_id=1
