import sqlite3
from config import DB_PATH   # adjust if needed

def get_all_labtests():
    con = sqlite3.connect(DB_PATH)
    con.row_factory = sqlite3.Row
    cur = con.cursor()

    labtests = cur.execute(
        "SELECT test_id, test_name, test_description, charges, discount FROM labtests"
    ).fetchall()

    con.close()
    return labtests

def get_labtest_by_id(labtest_id):
    con = sqlite3.connect(DB_PATH)
    con.row_factory = sqlite3.Row
    cur = con.cursor()

    labtest = cur.execute(
        """
        SELECT test_id, test_name, test_description, charges, discount FROM labtests
        WHERE labtest_id = ?
        """,
        (labtest_id,)
    ).fetchone()

    con.close()
    return{
        "labtest": labtest
     #   "schedules": schedules
        }
    