import sqlite3
from config import DB_PATH   # adjust if needed

def get_all_opdservices():
    con = sqlite3.connect(DB_PATH)
    con.row_factory = sqlite3.Row
    cur = con.cursor()

    opdservices = cur.execute(
        "SELECT service_id, service_name, service_description, service_duration, service_charges FROM opdservices"
    ).fetchall()

    con.close()
    return opdservices

def get_opdservice_by_id(opdservice_id):
    con = sqlite3.connect(DB_PATH)
    con.row_factory = sqlite3.Row
    cur = con.cursor()

    opdservice = cur.execute(
        """
        SELECT service_id, service_name, service_description, service_duration, service_charges FROM opdservices
        WHERE opdservice_id = ?
        """,
        (opdservice_id,)
    ).fetchone()

    con.close()
    return{
        "opdservice": opdservice
     #   "schedules": schedules
        }
    