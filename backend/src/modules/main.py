from flask import Flask, render_template, request, jsonify
from database import init_db, add_user, get_user
from backend.src.modules.ml_model import predict_stress

app = Flask(__name__)

# Initialize database
init_db()

@app.route("/")
def home():
    return render_template("index.html")

# User Signup
@app.route("/signup", methods=["POST"])
def signup():
    data = request.json
    result = add_user(data['username'], data['password'])
    return jsonify(result)

# User Login
@app.route("/login", methods=["POST"])
def login():
    data = request.json
    user = get_user(data['username'], data['password'])
    return jsonify({"success": bool(user)})

# User input submission & stress prediction
@app.route("/predict", methods=["POST"])
def predict():
    data = request.json
    stress_level = predict_stress(data)
    return jsonify({"stress_level": stress_level})

if __name__ == "__main__":
    app.run(debug=True)
