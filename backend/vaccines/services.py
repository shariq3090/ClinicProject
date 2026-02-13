import sqlite3
from config import DB_PATH   # adjust if needed

def get_all_vaccines():
    con = sqlite3.connect(DB_PATH)
    con.row_factory = sqlite3.Row
    cur = con.cursor()

    vaccines = cur.execute(
        "SELECT vaccine_id, vaccine_name, vaccine_description, batch_no, company, expiry_date, oral_injectable, age_group, duration_days FROM vaccines"
    ).fetchall()

    con.close()
    return vaccines

def get_vaccine_by_id(vaccine_id):
    con = sqlite3.connect(DB_PATH)
    con.row_factory = sqlite3.Row
    cur = con.cursor()

    vaccine = cur.execute(
        """
        "SELECT vaccine_id, vaccine_name, vaccine_description, batch_no, company, expiry_date, oral_injectable, age_group, duration_days
        FROM vaccines
        WHERE vaccine_id = ?
        """,
        (vaccine_id,)
    ).fetchone()

    con.close()
    return{
        "vaccine": vaccine
        #"schedules": schedules
        }
    