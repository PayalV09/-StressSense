import sqlite3
import matplotlib.pyplot as plt
from init_db import DB_NAME

def visualize_stress(user_id):
    """Display user's stress trends using a graph."""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("SELECT timestamp, stress_level FROM stress_data WHERE user_id=?", (user_id,))
    data = cursor.fetchall()
    
    conn.close()

    if not data:
        print("No data available for visualization.")
        return

    timestamps, stress_levels = zip(*data)

    plt.figure(figsize=(10,5))
    plt.plot(timestamps, stress_levels, marker='o', linestyle='-', color='b', label="Stress Level")
    plt.xlabel("Timestamp")
    plt.ylabel("Stress Level")
    plt.title("Stress Level Trend")
    plt.legend()
    plt.show()

if __name__ == "__main__":
    visualize_stress(1)
