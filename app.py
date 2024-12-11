import google.generativeai as genai
from flask import Flask, render_template, request, redirect, url_for
from dotenv import load_dotenv
import os
import sqlite3
import json
import uuid
import matplotlib.pyplot as plt
import io
import base64
import pandas as pd

app = Flask(__name__)
load_dotenv()
GOOGLE_API_KEY = os.environ.get('GOOGLE_API_KEY')  # Remember to set your GOOGLE_API_KEY
db_path = "health_risk_data.db"

genai.configure(api_key=GOOGLE_API_KEY)
model = genai.GenerativeModel('models/gemini-1.5-flash')

# Database functions
def create_db():
    with sqlite3.connect(db_path) as conn:
        conn.execute('''CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            personal_info TEXT,
            lifestyle TEXT,
            medical_history TEXT,
            symptoms TEXT,
            health_metrics TEXT,
            risk_status TEXT
        )''')
        conn.execute('''CREATE TABLE IF NOT EXISTS appointments (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            submission_id TEXT UNIQUE NOT NULL,
            appointment_date TEXT,
            appointment_time TEXT,
            doctor TEXT,
            notes TEXT,
            email TEXT
        )''')

if not os.path.exists(db_path):
    create_db()

def save_user_data(personal_info, lifestyle, medical_history, symptoms, health_metrics, risk_status):
    with sqlite3.connect(db_path) as conn:
        try:
            conn.execute('''INSERT INTO users (personal_info, lifestyle, medical_history, symptoms, health_metrics, risk_status)
                            VALUES (?, ?, ?, ?, ?, ?)''',
                         (json.dumps(personal_info), json.dumps(lifestyle), json.dumps(medical_history),
                          json.dumps(symptoms), json.dumps(health_metrics), risk_status))
            conn.commit()
        except Exception as e:
            return f"Database error: {e}"

def calculate_bmi(height, weight):
    try:
        height_meters = float(height) / 100
        weight_kg = float(weight)
        bmi = round(weight_kg / (height_meters ** 2), 1)
        return bmi
    except (ValueError, TypeError):
        return None

def get_gemini_response(prompt):
    try:
        response = model.generate_content(prompt)
        return response.text.strip()
    except Exception as e:
        return f"Error communicating with Gemini API: {e}"

def save_appointment_data(submission_id, appointment_date, appointment_time, doctor, notes, email):
    with sqlite3.connect(db_path) as conn:
        try:
            conn.execute('''INSERT INTO appointments (submission_id, appointment_date, appointment_time, doctor, notes, email)
                            VALUES (?, ?, ?, ?, ?, ?)''',
                         (submission_id, appointment_date, appointment_time, doctor, notes, email))
            conn.commit()
        except Exception as e:
            return f"Database error: {e}"

@app.route('/', methods=['GET', 'POST'])
def index():
    error = None
    if request.method == 'POST':
        try:
            personal_info = {
                "name": request.form['name'],
                "email": request.form['email'],
                "phone": request.form['phone'],
                "dob": request.form['dob'],
                "gender": request.form['gender'],
                "address": request.form['address'],
            }
            lifestyle = {
                "smoke": request.form['smoke'],
                "alcohol": request.form['alcohol'],
                "exercise": request.form['exercise'],
                "diet": request.form['diet'],
                "sleep": request.form.get('sleep', ''),
            }
            medical_history = {
                "family_history": request.form.getlist('family_history'),
                "chronic_diseases": request.form.getlist('chronic_diseases'),
                "medications": request.form.get('medications', ''),
                "surgeries": request.form.get('surgeries', ''),
            }
            symptoms = request.form.getlist('symptoms')
            health_metrics = {
                "height": request.form.get('height', ''),
                "weight": request.form.get('weight', ''),
                "blood_pressure": request.form.get('blood_pressure', ''),
            }

            bmi = calculate_bmi(health_metrics.get('height', 0), health_metrics.get('weight', 0))
            if bmi:
                health_metrics['bmi'] = bmi

            prompt = (
                f"Analyze the following health data:\n"
                f"Personal Info: {personal_info}\n"
                f"Lifestyle: {lifestyle}\n"
                f"Medical History: {medical_history}\n"
                f"Symptoms: {symptoms}\n"
                f"Health Metrics: {health_metrics}\n"
            )

            insights = get_gemini_response(prompt)
            risk_status = "At Risk" if "risk" in insights.lower() else "Healthy"

            db_error = save_user_data(personal_info, lifestyle, medical_history, symptoms, health_metrics, risk_status)
            if db_error:
                error = db_error
            else:
                return render_template('result.html', insights=insights, risk_status=risk_status, email=personal_info.get('email', ''))
        except Exception as e:
            error = f"An error occurred: {e}"

    return render_template('index.html', error=error)

@app.route('/result', methods=['GET'])
def result():
    email = request.args.get('email')
    return render_template('result.html', email=email)

@app.route('/appointment', methods=['GET', 'POST'])
def appointment():
    if request.method == 'POST':
        submission_id = str(uuid.uuid4())
        appointment_date = request.form['appointment_date']
        appointment_time = request.form['appointment_time']
        doctor = request.form['doctor']
        notes = request.form.get('notes')
        email = request.form['email']

        db_error = save_appointment_data(submission_id, appointment_date, appointment_time, doctor, notes, email)
        if db_error:
            return f"Error saving appointment data: {db_error}"
        return redirect(url_for('appointment_confirmation'))
    return render_template('appointment.html')

@app.route('/appointment_confirmation')
def appointment_confirmation():
    return render_template('appointment_confirmation.html')

@app.route('/admin', methods=['GET'])
def admin_panel():
    with sqlite3.connect(db_path) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users")
        user_data = cursor.fetchall()
        cursor.execute("SELECT * FROM appointments")
        appointments = cursor.fetchall()

    # Appointment Chart
    appointment_counts = {}
    for appt in appointments:
        doctor = appt[4]
        appointment_counts[doctor] = appointment_counts.get(doctor, 0) + 1
    labels = list(appointment_counts.keys())
    sizes = list(appointment_counts.values())

    fig, ax = plt.subplots()
    ax.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=90)
    ax.axis('equal')
    img_appt = io.BytesIO()
    plt.savefig(img_appt, format='png')
    img_appt.seek(0)
    plot_url_appt = base64.b64encode(img_appt.getvalue()).decode()
    plt.close(fig) #Close the figure to prevent memory leaks


    # Risk Status Chart
    risk_counts = {}
    for user in user_data:
        risk_status = user[6]
        risk_counts[risk_status] = risk_counts.get(risk_status, 0) + 1

    risk_labels = list(risk_counts.keys())
    risk_sizes = list(risk_counts.values())

    fig, ax = plt.subplots()
    ax.pie(risk_sizes, labels=risk_labels, autopct='%1.1f%%', startangle=90)
    ax.axis('equal')
    img_risk = io.BytesIO()
    plt.savefig(img_risk, format='png')
    img_risk.seek(0)
    plot_url_risk = base64.b64encode(img_risk.getvalue()).decode()
    plt.close(fig) #Close the figure to prevent memory leaks

    return render_template('admin.html', users=user_data, appointments=appointments, 
                           plot_url_appt=plot_url_appt, plot_url_risk=plot_url_risk)

if __name__ == '__main__':
    app.run(debug=True)

if __name__ == '__main__':
    app.run(debug=True)
