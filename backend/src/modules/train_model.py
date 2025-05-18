import os
import pickle
from sklearn.ensemble import RandomForestClassifier
from sklearn.datasets import make_classification
from sklearn.model_selection import train_test_split

# Generate a sample dataset (replace with actual data)
X, y = make_classification(n_samples=100, n_features=5, random_state=42)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Train a simple model
model = RandomForestClassifier()
model.fit(X_train, y_train)

# Define the save path for the model
model_dir = os.path.join(os.path.dirname(__file__), "models")
os.makedirs(model_dir, exist_ok=True)  # Create the directory if it doesn't exist

# Specify the full path to save the model
model_path = os.path.join(model_dir, "stress_model.pkl")

# Save the trained model using pickle
with open(model_path, "wb") as file:
    pickle.dump(model, file)

print(f"Model saved successfully at: {model_path}")
