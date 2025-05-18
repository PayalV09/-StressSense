import os
import pickle
from pathlib import Path
import pickle

def load_model():
    base_dir = Path(__file__).resolve().parent
    model_path = base_dir / "models" / "stress_model.pkl"
    print(f"📦 Loading model from: {model_path}")

    if not model_path.exists():
        print("❌ Error: Model file not found!")
        return None

    try:
        with model_path.open("rb") as f:
            model = pickle.load(f)
        print("✅ Model loaded successfully!")
        return model
    except Exception as e:
        print(f"❌ Error loading model: {e}")
        return None
