from datetime import datetime, timedelta
import sqlite3
import os
import uuid
from flask import abort, jsonify, redirect, render_template, request, url_for
from config import DB_PATH   # or wherever DB_PATH is
from doctors.services import get_doctor_by_id


def appointment():
     return 'abc'    

def get_doctor_by_id(doctor_id):
    con = sqlite3.connect(DB_PATH)
    con.row_factory = sqlite3.Row
    cur = con.cursor()

    doctor = cur.execute(
        """
        SELECT doctor_id, full_name, gender, specialization, qualification, experience_years, consultation_fee
        FROM doctors
        WHERE doctor_id = ?
        """,
        (doctor_id,)
    ).fetchone()

    # Doctor schedule (MULTIPLE rows)
    schedules = cur.execute("""
        SELECT             
            room_no,
            visit_days,
            visit_start_time,
            visit_end_time
        FROM doctors_operational
        WHERE doctor_id = ?
        ORDER BY visit_days
    """, (doctor_id,)).fetchall()

    con.close()
    return{
        "doctor": doctor,
        "schedules": schedules
        }

def available_slots(doctor_id):      
    date = request.args.get("date")
    slots = get_available_slots(doctor_id, date)
    return jsonify(slots)

def get_available_slots(doctor_id, selected_date):    
    con = sqlite3.connect(DB_PATH)
    con.row_factory = sqlite3.Row
    cur = con.cursor()
    
    weekday = datetime.strptime(selected_date, "%Y-%m-%d").strftime("%A")
    
    schedules = cur.execute("""
        SELECT visit_start_time, visit_end_time, slot_duration_minutes
        FROM doctors_operational
        WHERE doctor_id = ?
        AND LOWER(visit_days) LIKE LOWER(?)
    """, (doctor_id, f"%{weekday}%")).fetchall()
    
    if not schedules:
        print("No schedules")
        con.close()
        return []
    
    all_slots = []

    for schedule in schedules:
        all_slots.extend(
            generate_time_slots(
                schedule["visit_start_time"],
                schedule["visit_end_time"],
                schedule["slot_duration_minutes"]
            )
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

def save_appointment(doctor_id):    
    #confirmation_no = f"APT-{uuid.uuid4().hex[:8].upper()}"    
    confirmation_no = generate_confirmation_no(doctor_id, request.form["appointment_date"])
    print(confirmation_no)
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
        abort(400, "Time slot already booked")
        #return "Time slot already booked", 400
    

    cur.execute("""
        INSERT INTO appointments (
            confirmation_no,    
            doctor_id,
            patient_name,
            patient_phone,
            patient_email,
            appointment_date,
            visit_start_time,
            visit_end_time
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    """, (confirmation_no, doctor_id, name, phone, email, date, start, end))

    appointment_id = cur.lastrowid

    con.commit()    
    con.close()

    return appointment_id  

def appointment_success(appointment_id):
    #print("Inside Appointment Success. Appointment Id: ", appointment_id)    
    con = sqlite3.connect(DB_PATH)
    con.row_factory = sqlite3.Row   # ✅ THIS IS THE KEY LINE
    cur = con.cursor()

    appointment = cur.execute("""
        SELECT
            a.appointment_id,
            a.confirmation_no,
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
        print("Error: No appointment details available")

    return appointment

def generate_confirmation_no(doctor_id, appointment_date):
    con = sqlite3.connect(DB_PATH)
    cur = con.cursor()

    # Count today's appointments for this doctor
    cur.execute("""
        SELECT COUNT(*) 
        FROM appointments
        WHERE doctor_id = ?
        AND appointment_date = ?
    """, (doctor_id, appointment_date))

    count = cur.fetchone()[0] or 0
    running_no = count + 1

    date_part = datetime.strptime(
        appointment_date, "%Y-%m-%d"
    ).strftime("%Y%m%d")

    confirmation_no = f"APT-{doctor_id}-{date_part}-{running_no:03d}"

    con.close()
    return confirmation_no