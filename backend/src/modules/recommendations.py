def get_recommendations(stress_level):
    """Suggests mental health tips based on stress level."""
    if stress_level < 4:
        return "😀 Low Stress: Keep up your good habits!"
    elif 4 <= stress_level < 7:
        return "😐 Moderate Stress: Try meditation, exercise, and a balanced diet."
    else:
        return "😟 High Stress: Consider yoga, relaxation techniques, or seeking professional help."

if __name__ == "__main__":
    print(get_recommendations(6))  # Example recommendation
