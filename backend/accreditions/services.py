import sqlite3
from config import DB_PATH   # adjust if needed

def get_all_accreditions():
    con = sqlite3.connect(DB_PATH)
    con.row_factory = sqlite3.Row
    cur = con.cursor()

    accreditions = cur.execute(
        "SELECT accredition_id, accredition_name, accredition_description, awarding_body, awarded_year FROM accreditions"
    ).fetchall()

    con.close()
    return accreditions

def get_accredition_by_id(accredition_id):
    con = sqlite3.connect(DB_PATH)
    con.row_factory = sqlite3.Row
    cur = con.cursor()

    accredition = cur.execute(
        """
        "SELECT accredition_id, accredition_name, accredition_description, awarding_body, awarded_year, validity_years FROM accreditions
        FROM accreditions
        WHERE accredition_id = ?
        """,
        (accredition_id,)
    ).fetchone()

    con.close()
    return{
        "accredition": accredition
        #"schedules": schedules
        }
    