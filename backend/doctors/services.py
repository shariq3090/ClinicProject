import sqlite3
from config import DB_PATH   # adjust if needed

def get_all_doctors():
    con = sqlite3.connect(DB_PATH)
    con.row_factory = sqlite3.Row
    cur = con.cursor()

    doctors = cur.execute(
        "SELECT doctor_id, full_name, gender, specialization, qualification, experience_years FROM doctors"
    ).fetchall()

    con.close()
    return doctors

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
    