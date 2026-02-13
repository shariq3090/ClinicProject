import datetime
import uuid
from flask import Flask, abort, jsonify, redirect, render_template, request, url_for
import sqlite3
import os
from datetime import datetime, timedelta
from accreditions.routes import accredition_bp
from doctors.routes import doctor_bp
from medicalstaffs.routes import medicalstaff_bp
from opdservices.routes import opdservice_bp
from labtests.routes import labtest_bp
from procedures.routes import procedure_bp
from vaccines.routes import vaccine_bp
from appointments.routes import appointment_bp

app = Flask(__name__)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
#DB_PATH = os.path.join(BASE_DIR, "clinic.db")
DB_PATH = os.environ.get(
    "DB_PATH",
    os.path.join(BASE_DIR, "clinic.db")
)

app.register_blueprint(accredition_bp)
app.register_blueprint(doctor_bp)
app.register_blueprint(medicalstaff_bp)
app.register_blueprint(opdservice_bp)
app.register_blueprint(labtest_bp)
app.register_blueprint(procedure_bp)
app.register_blueprint(vaccine_bp)
app.register_blueprint(appointment_bp)

@app.route("/")
def index():
    return render_template("index.html")
    #return "Grace Clinic is running"

@app.route("/introduction")
def introduction():
    return render_template("introduction.html")

@app.route("/about")
def about():
    return render_template("about.html")

@app.route("/patient")
def patients():
    con = sqlite3.connect(DB_PATH)
    cur = con.cursor()
    cur.execute("SELECT name, age, gender, phone FROM patients")
    rows = cur.fetchall()
    con.close()

    patients_list = []
    for row in rows:
        patients_list.append({
            "name": row[0],
            "age": row[1],
            "gender": row[2],
            "phone": row[3],
        })

    return render_template("patients.html", patients=patients_list)

@app.route("/visits")
def visits():
    con = sqlite3.connect(DB_PATH)
    cur = con.cursor()
    cur.execute("SELECT patient_id, visit_date, doctor_name, diagnosis, prescription FROM visits")
    rows = cur.fetchall()
    con.close()

    visits_list = []
    for row in rows:
        visits_list.append({
            "patient_id": row[0],
            "visit_date": row[1],
            "doctor_name": row[2],
            "diagnosis": row[3],
            "prescription": row[4]
        })

    return render_template("visits.html", visits=visits_list)

################## Other Functions #######################

def save_appointment123(doctor_id):
    print("Inside Save")
    confirmation_no = f"APT-{uuid.uuid4().hex[:8].upper()}"
    name = request.form["patient_name"]
    phone = request.form["patient_phone"]
    email = request.form.get("patient_email")
    date = request.form["appointment_date"]
    slot = request.form["slot"]   # "09:00|09:15"
    visit_start_time, visit_end_time = slot.split("|")
    #start = request.form["visit_start_time"]
    #end = request.form["visit_end_time"]
    start = visit_start_time
    end = visit_end_time

    con = sqlite3.connect(DB_PATH)
    cur = con.cursor()

    # ❌ Check overlapping appointments
    conflict = cur.execute("""
        SELECT 1 FROM appointments
        WHERE doctor_id = ?
        AND appointment_date = ?
        AND (
            visit_start_time < ?
            AND visit_end_time > ?
        )
    """, (doctor_id, date, end, start)).fetchone()

    if conflict:
        con.close()
        return "Time slot already booked", 400

    cur.execute("""
        INSERT INTO appointments (
            doctor_id,
            patient_name,
            patient_phone,
            patient_email,
            appointment_date,
            visit_start_time,
            visit_end_time
        ) VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (doctor_id, name, phone, email, date, start, end))

    appointment_id = cur.lastrowid

    con.commit()
    con.close()

    return appointment_id    

    #return redirect(url_for("appointment_success.html"))
    #return render_template("appointment_success.html")

@app.route("/doctors_old/<int:doctor_id>/available-slots")
def available_slots(doctor_id):      
    date = request.args.get("date")
    slots = get_available_slots(doctor_id, date)
    return jsonify(slots)

def get_available_slots(doctor_id, selected_date):
    con = sqlite3.connect(DB_PATH)
    con.row_factory = sqlite3.Row
    cur = con.cursor()
    
    weekday = datetime.strptime(selected_date, "%Y-%m-%d").strftime("%A")
    #print("inside get_available_slots", doctor_id, weekday)
    schedule = cur.execute("""
        SELECT visit_start_time, visit_end_time, slot_duration_minutes
        FROM doctors_operational
        WHERE doctor_id = ?
        AND visit_days LIKE ?
    """, (doctor_id, f"%{weekday}%")).fetchone()
    
    if not schedule:
        return []

    all_slots = generate_time_slots(
        schedule["visit_start_time"],
        schedule["visit_end_time"],
        schedule["slot_duration_minutes"]
    )
    
    booked = cur.execute("""
        SELECT visit_start_time, visit_end_time
        FROM appointments
        WHERE doctor_id = ?
        AND appointment_date = ?
    """, (doctor_id, selected_date)).fetchall()

    booked_slots = {(b["visit_start_time"], b["visit_end_time"]) for b in booked}

    available_slots = [
        slot for slot in all_slots if slot not in booked_slots
    ]

    con.close()
    return available_slots

def generate_time_slots(start_time, end_time, duration):
    slots = []
    current = datetime.strptime(start_time, "%H:%M")
    end = datetime.strptime(end_time, "%H:%M")

    while current + timedelta(minutes=duration) <= end:
        slot_start = current.strftime("%H:%M")
        slot_end = (current + timedelta(minutes=duration)).strftime("%H:%M")
        slots.append((slot_start, slot_end))
        current += timedelta(minutes=duration)

    return slots
def save_appointment456(doctor_id):
    name = request.form["patient_name"]
    phone = request.form["patient_phone"]
    email = request.form.get("patient_email")
    date = request.form["appointment_date"]
    slot = request.form["slot"]

    visit_start_time, visit_end_time = slot.split("|")

    con = sqlite3.connect(DB_PATH)
    cur = con.cursor()

    cur.execute("""
        INSERT INTO appointments (
            doctor_id,
            patient_name,
            patient_phone,
            patient_email,
            appointment_date,
            visit_start_time,
            visit_end_time
        ) VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (doctor_id, name, phone, email, date, visit_start_time, visit_end_time))

    appointment_id = cur.lastrowid   # ✅ IMPORTANT

    con.commit()
    con.close()

    return appointment_id

@app.route("/appointment-success/<int:appointment_id>")
def appointment_success(appointment_id):
    con = sqlite3.connect(DB_PATH)
    cur = con.cursor()

    appointment = cur.execute("""
        SELECT             
            a.patient_name,
            a.appointment_date,
            a.visit_start_time,
            a.visit_end_time,
            d.full_name            
        FROM appointments a
        JOIN doctors d ON d.doctor_id = a.doctor_id
        WHERE a.appointment_id = ?
    """, (appointment_id,)).fetchone()

    con.close()

    if not appointment:
        abort(404)

    return render_template(
        "appointment_success.html",
        appointment={      
            "patient_name": appointment[0],
            "date": appointment[1],
            "start": appointment[2],
            "end": appointment[3],
            "full_name": appointment[4]
            #"full_name": appointment[4]
        }
    )

@app.template_filter('dd_mmm_yyyy')
def dd_mmm_yyyy(value):
    if not value:
        return ''
    return datetime.strptime(value, '%Y-%m-%d').strftime('%d-%b-%Y')


if __name__ == "__main__":
    app.run(debug=True) 