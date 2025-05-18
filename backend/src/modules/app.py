import os
import pickle
import numpy as np
from flask import Flask, render_template, request, redirect, session, flash, url_for, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from werkzeug.security import generate_password_hash, check_password_hash
from textblob import TextBlob
import seaborn as sns
import matplotlib.pyplot as plt
from datetime import datetime
from ml_model import load_model
from werkzeug.security import generate_password_hash, check_password_hash




# ------------------ Sentiment Function ------------------
def get_sentiment_score(text):
    if text:
        return TextBlob(text).sentiment.polarity  # Range: -1 to 1
    return 0

# ------------------ Flask App Initialization ------------------
BASE_DIR = os.path.abspath(os.path.dirname(__file__))
TEMPLATE_DIR = r"D:\Stress Sense\frontend\templates"
STATIC_DIR = r"D:\Stress Sense\frontend\static"

app = Flask(__name__, template_folder=TEMPLATE_DIR, static_folder=STATIC_DIR)
app.secret_key = "your_secret_key"

# ------------------ Database Configuration ------------------
DB_PATH = os.path.join(BASE_DIR, "stress_db.sqlite")
app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///{DB_PATH}"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)
migrate = Migrate(app, db)

# ------------------ Database Models ------------------
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    phone_number = db.Column(db.String(15), unique=True, nullable=False)  # Ensure this field is defined


class StressRecord(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    mood = db.Column(db.String(50), nullable=True)
    sleep_hours = db.Column(db.Float, nullable=True)
    coffee = db.Column(db.Integer, nullable=True)
    water_intake = db.Column(db.Integer, nullable=True)
    activities = db.Column(db.String(100), nullable=True)
    work_hours = db.Column(db.Float, nullable=True)
    feelings = db.Column(db.Text, nullable=True)
    stress_level = db.Column(db.Float, nullable=True)
    occupation = db.Column(db.String(100), nullable=True)  # <-- ADD THIS
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)



class StressAssessment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    heart_rate = db.Column(db.Float, nullable=False)
    sleep_hours = db.Column(db.Float, nullable=False)
    work_hours = db.Column(db.Float, nullable=False)
    additional_feelings = db.Column(db.Text, nullable=True)

# models/stress.py
def get_all_users_with_records():
    query = """
    SELECT user_id, timestamp, stress_level 
    FROM stress_data 
    ORDER BY user_id, timestamp DESC
    """
    cursor.execute(query)
    rows = cursor.fetchall()
    return rows







# ------------------ Load ML Model ------------------
def load_model():
    model_path = os.path.join(BASE_DIR, "models", "stress_model.pkl")
    if not os.path.exists(model_path):
        print(f"⚠️ Model file not found at: {model_path}")
        return None
    try:
        with open(model_path, "rb") as file:
            model = pickle.load(file)
        print("✅ ML Model loaded successfully!")
        return model
    except Exception as e:
        print(f"❌ Error loading model: {e}")
        return None


# ------------------ Routes ------------------
@app.route("/")
def landing():
    return render_template("landing.html")
########### privacy policy ################
@app.route('/privacy-policy')                
def privacy_policy():
    return render_template('privacy_policy.html')
############ contact form ##############
@app.route('/contact', methods=['POST'])
def contact():
    name = request.form['name']
    email = request.form['email']
    message = request.form['message']
    # You can save this data to a database or send an email

    flash('Message sent successfully!', 'success')
    return redirect(url_for('landing'))  # ✅ Corrected from 'home' to 'landing'












@app.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        if not username or not password:
            flash("Username and password are required!", "danger")
            return redirect(url_for("signup"))
        if User.query.filter_by(username=username).first():
            flash("Username already exists!", "danger")
            return redirect(url_for("signup"))
        hashed_password = generate_password_hash(password)
        new_user = User(username=username, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()
        flash("Signup successful!", "success")
        return redirect(url_for("login"))
    return render_template("signup.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        user = User.query.filter_by(username=username).first()
        if user and check_password_hash(user.password, password):
            session["user_id"] = user.id
            flash("Login successful!", "success")
            return redirect(url_for("data_collection"))
        flash("Invalid credentials", "danger")
    return render_template("login.html")

@app.route("/logout")
def logout():
    session.clear()
    flash("Logged out successfully!", "info")
    return redirect(url_for("landing"))

@app.route("/data-collection", methods=["GET", "POST"])
def data_collection():
    if "user_id" not in session:
        flash("Please log in first!", "warning")
        return redirect(url_for("login"))

    if request.method == "POST":
        try:
            # Get inputs from the form
            heart_rate = float(request.form.get("heartRate"))
            sleep_hours = float(request.form.get("sleepHours"))
            work_hours = float(request.form.get("workHours"))
            feelings = request.form.get("feelings", "")
            
            # Convert feelings to sentiment score
            sentiment_score = get_sentiment_score(feelings)

            # Save raw data in StressAssessment table
            new_entry = StressAssessment(
                user_id=session["user_id"],
                heart_rate=heart_rate,
                sleep_hours=sleep_hours,
                work_hours=work_hours,
                additional_feelings=feelings
            )
            db.session.add(new_entry)
            db.session.commit()
            

            # Check model availability
            if model is None:
                flash("Model not loaded, unable to process data.", "danger")
                return redirect(url_for("data_collection"))

            # Predict stress level using ML model
            input_data = np.array([[heart_rate, sleep_hours, work_hours, sentiment_score]])
            prediction = model.predict(input_data)[0]

            # Save prediction in StressRecord
            stress_record = StressRecord(user_id=session["user_id"], stress_level=prediction)
            db.session.add(stress_record)
            db.session.commit()

            flash("Stress level predicted successfully!", "success")
            return redirect(url_for("dashboard"))  # ✅ go directly to dashboard

        except ValueError:
            flash("Invalid input! Please enter valid numbers.", "danger")
        except Exception as e:
            flash(f"Error in processing input: {e}", "danger")

    return render_template("data_collection.html")

@app.route("/submit-stress-data", methods=["POST"])
def submit_stress_data():
    if "user_id" not in session:
        return jsonify({"success": False, "message": "Please log in to submit data!"}), 401

    try:
        data = request.get_json()
        mood = data.get("mood", "").strip()
        sleep_hours = float(data.get("sleepHours", 0))
        coffee = int(data.get("coffee", 0))
        water_intake = int(data.get("waterIntake", 0))
        activities = data.get("activities", "").strip()
        custom_activity = data.get("customActivity", "").strip()
        work_hours = float(data.get("workHours", 0))
        feelings = data.get("feelings", "").strip()
        final_activity = custom_activity if activities == "Other" else activities

        new_entry = StressRecord(
            user_id=session["user_id"],
            mood=mood,
            sleep_hours=sleep_hours,
            coffee=coffee,
            water_intake=water_intake,
            activities=final_activity,
            work_hours=work_hours,
            feelings=feelings
        )
        db.session.add(new_entry)
        db.session.commit()

        if model is None:
            return jsonify({"success": False, "message": "Model not loaded"}), 500

        mood_val = 1 if mood.lower() == "happy" else 0
        feelings_val = 1 if feelings.lower() == "positive" else 0
        input_features = np.array([[sleep_hours, coffee, water_intake, work_hours, mood_val, feelings_val]])
        prediction = model.predict(input_features)[0]

        if prediction > 0.7:
            stress_label = "high"
        elif prediction > 0.4:
            stress_label = "moderate"
        else:
            stress_label = "low"

        return jsonify({
            "success": True,
            "prediction": round(prediction, 2),
            "stress_level": stress_label
        })

    except ValueError:
        return jsonify({"success": False, "message": "Invalid input values!"}), 400
    except Exception as e:
        db.session.rollback()
        return jsonify({"success": False, "message": f"Server error: {str(e)}"}), 500
@app.route("/predict-stress", methods=["GET", "POST"])
def predict_stress():
    if request.method == "POST":
        try:
            mood = request.form.get('mood')
            sleep_hours = float(request.form.get('sleepHours'))
            coffee = int(request.form.get('coffee'))
            water = int(request.form.get('waterIntake'))
            work_hours = float(request.form.get('workHours', 0))
            feelings = request.form.get('feelings')
            sentiment_score = get_sentiment_score(feelings)

            stress_score = 0
            if sleep_hours < 6:
                stress_score += 2
            if coffee > 3:
                stress_score += 1
            if work_hours > 8:
                stress_score += 2
            if sentiment_score < -0.3:
                stress_score += 2
            elif sentiment_score < 0:
                stress_score += 1

            if stress_score <= 2:
                stress_label = "Low"
                stress_class = "low"
            elif stress_score <= 4:
                stress_label = "Moderate"
                stress_class = "moderate"
            else:
                stress_label = "High"
                stress_class = "high"

            # ✅ Save to database
            if "user_id" in session:
                new_record = StressRecord(
                    user_id=session["user_id"],
                    mood=mood,
                    sleep_hours=sleep_hours,
                    coffee=coffee,
                    water_intake=water,
                    work_hours=work_hours,
                    feelings=feelings,
                    stress_level=stress_score,
                    timestamp=datetime.now(timezone.utc)
                )
                db.session.add(new_record)
                db.session.commit()
                print("✅ Stress record saved.")
            else:
                print("⚠️ User not logged in. Stress data not saved.")

            # ✅ Return JSON result
            return jsonify({
                'success': True,
                'stress_level': stress_label,
                'stress_class': stress_class,
                'score': f"{stress_score}/6"
            })

        except Exception as e:
            return jsonify({"success": False, "message": f"Server error: {str(e)}"}), 500

    return render_template("predict_stress.html")

@app.route("/prediction")
def show_prediction():
    stress_level = request.args.get('level')
    stress_class = request.args.get('class')
    return render_template('prediction.html', stress_level=stress_level, stress_class=stress_class)
def get_stress_level_category(level):
    if level >= 7:
        return "High"
    elif level >= 4:
        return "Moderate"
    elif level >= 1:
        return "Low"
    else:
        return "None"

@app.route("/dashboard")
def dashboard():
    if "user_id" not in session:
        flash("Please log in first!", "warning")
        return redirect(url_for("login"))

    try:
        user_id = session["user_id"]
        print(f"✅ Session user ID: {user_id}")

        # Fetch records
        stress_records = (
            StressRecord.query
            .filter_by(user_id=user_id)
            .order_by(StressRecord.timestamp.desc())
            .all()
        )

        print("📊 Number of stress records fetched:", len(stress_records))
        for r in stress_records:
            print(f"🕒 Timestamp: {r.timestamp}, 😟 Stress Level: {r.stress_level}")

        # Convert records with derived level
        records_json = [
            {
                "timestamp": r.timestamp.strftime("%Y-%m-%d %H:%M:%S"),
                "stress_level": r.stress_level,
                "level": get_stress_level_category(r.stress_level)
            }
            for r in stress_records
        ]

        return render_template(
            "dashboard.html",
            records=stress_records,
            records_json=records_json
        )

    except Exception as e:
        print(f"❌ Exception occurred in /dashboard: {e}")
        flash(f"Error loading dashboard: {e}", "danger")


#######  dashboard 1 #######
@app.route("/dashboard1")
def dashboard1():
    if "user_id" not in session:
        flash("Please log in first!", "warning")
        return redirect(url_for("login"))

    try:
        user_id = session["user_id"]

        stress_records = (
            StressRecord.query
            .filter_by(user_id=user_id)
            .order_by(StressRecord.timestamp.desc())
            .all()
        )

        # Convert to JSON for charts
        records_json = [
            {
                "timestamp": r.timestamp.strftime("%Y-%m-%d %H:%M:%S"),
                "stress_level": r.stress_level,
                "level": get_stress_level_category(r.stress_level)
            }
            for r in stress_records
        ]

        return render_template(
            "dashboard1.html",
            records_json=records_json
        )

    except Exception as e:
        print(f"❌ Exception in /dashboard1: {e}")
        flash(f"Error loading stress trends: {e}", "danger")
        return redirect(url_for("dashboard"))


@app.route("/recommendations")
def recommendations():
    if "user_id" not in session:
        flash("Please log in first!", "warning")
        return redirect(url_for("login"))

    try:
        user_id = session["user_id"]
        latest_record = StressRecord.query.filter_by(user_id=user_id).order_by(StressRecord.timestamp.desc()).first()

        if latest_record:
            stress_level = latest_record.stress_level

            # Define recommendations based on stress level
            if stress_level >= 7:
                recommendations = {
                    "relaxation_techniques": "It's important to manage your stress actively. Try deep breathing, guided meditation, or even mindfulness exercises to calm your mind and body. Regular practice can help reduce stress.",
                    "healthy_lifestyle": "Focus on incorporating regular exercise, a balanced diet, and quality sleep into your daily routine. These practices will help improve both your physical and mental health."
                }
            elif stress_level >= 4:
                recommendations = {
                    "relaxation_techniques": "Stress can be challenging, but small steps like practicing light meditation or using breathing exercises can help you relax and regain control over your emotions.",
                    "healthy_lifestyle": "Ensure you maintain a healthy routine by eating well, staying hydrated, and getting enough rest. Regular movement like walking or stretching can also improve your stress levels."
                }
            else:
                recommendations = {
                    "relaxation_techniques": "You’re doing great! Keeping stress at bay is key. Meditation and simple breathing exercises can further enhance your relaxation. Keep up the good work!",
                    "healthy_lifestyle": "Continue with your healthy habits! Focus on maintaining quality sleep, staying hydrated, and keeping up with physical activities to stay stress-free."
                }

            return render_template("recommendations.html", recommendations=recommendations, stress_level=stress_level)
        else:
            flash("No stress data available.", "warning")
            return redirect(url_for("dashboard"))
    
    except Exception as e:
        flash(f"Error fetching recommendations: {e}", "danger")
        return redirect(url_for("dashboard"))


#########temproory 
@app.route("/view-all-records")
def view_all_records():
    records = StressRecord.query.all()
    return "<br>".join([f"User ID: {r.user_id}, Stress Level: {r.stress_level}" for r in records])



##########         ADMIN     ###########
@app.route('/admin/login', methods=['GET', 'POST'])
def admin_login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        # Hardcoded credentials (consider hashing password in a real app)
        if username == "Adminstresssense" and password == "stresssense":
            session['admin'] = True
            return redirect(url_for('admin_dashboard'))
        else:
            flash("Invalid credentials", "danger")
    return render_template("admin_login.html")

# Admin dashboard route
@app.route('/admin/dashboard')
def admin_dashboard():
    if 'admin' in session:
        users = User.query.all()  # Retrieve all users from the database
        return render_template("admin_dashboard.html", users=users)
    else:
        return redirect(url_for('admin_login'))

# Admin logout route
@app.route('/admin/logout')
def admin_logout():
    session.pop('admin', None)
    return redirect(url_for("landing.html"))

# Upload model route
@app.route('/admin/upload_model', methods=['POST'])
def upload_model():
    if 'admin' in session:
        file = request.files['model']
        if file:
            filepath = os.path.join("src/modules/models", "stress_model.pkl")
            file.save(filepath)
            flash("Model updated successfully!", "success")
        return redirect(url_for('admin_dashboard'))
    return redirect(url_for('admin_login'))

# Add recommendation route
@app.route('/admin/add_recommendation', methods=['POST'])
def add_recommendation():
    if 'admin' in session:
        recommendation = request.form['recommendation']
        with open("recommendations.txt", "a") as f:
            f.write(recommendation + "\n")
        flash("Recommendation added.", "success")
        return redirect(url_for('admin_dashboard'))
    return redirect(url_for('admin_login'))





############test 






@app.route("/add-test-record")
def add_test_record():
    if "user_id" not in session:
        flash("Please log in first!", "warning")
        return redirect(url_for("login"))

    test_record = StressRecord(
        user_id=session["user_id"],
        mood="Calm",
        sleep_hours=7.5,
        coffee=1,
        water_intake=8,
        activities="Reading, Walking",
        work_hours=6,
        feelings="Felt relaxed after walk",
        stress_level=1.2,
        timestamp=datetime.utcnow()
    )
    db.session.add(test_record)
    db.session.commit()

    print("✅ Test record added for user_id:", session["user_id"])
    return redirect(url_for("dashboard"))


# ------------------ Main App Runner ------------------
if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    print(f"✅ Database initialized at {DB_PATH}")
    app.run(debug=True)
