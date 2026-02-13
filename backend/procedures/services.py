import sqlite3
from config import DB_PATH   # adjust if needed

def get_all_procedures():
    con = sqlite3.connect(DB_PATH)
    con.row_factory = sqlite3.Row
    cur = con.cursor()

    procedures = cur.execute(
        "SELECT service_id, service_name, service_description, service_duration, service_charges FROM opdservices"
    ).fetchall()

    con.close()
    return procedures

def get_procedure_by_id(procedure_id):
    con = sqlite3.connect(DB_PATH)
    con.row_factory = sqlite3.Row
    cur = con.cursor()

    procedure = cur.execute(
        """
        SELECT service_id, service_name, service_description, service_duration, service_charges FROM opdservices
        WHERE opdservice_id = ?
        """,
        (procedure_id,)
    ).fetchone()

    con.close()
    return{
        "procedure": procedure
     #   "schedules": schedules
        }
    