import sqlite3

con = sqlite3.connect("clinic.db")
cur = con.cursor()

cur.execute("""
CREATE TABLE IF NOT EXISTS doctors (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    specialization TEXT
)
""")

#cur.execute("""
# INSERT INTO doctors (name, specialization)
# VALUES ('Dr. Mira Khan', 'General Physician')
# """)

cur.execute("""
CREATE TABLE IF NOT EXISTS lab_tests (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    test_name TEXT,
    description TEXT
)
""")

#cur.execute("""
#INSERT INTO lab_tests (test_name, description)
#VALUES ('Blood Sugar', 'Fasting and Random blood sugar test')
#""")

cur.execute("""
INSERT INTO lab_tests (test_name, description)
VALUES ('HB1AC', '3 month blood sugar test')
""")

cur.execute("""
INSERT INTO lab_tests (test_name, description)            
VALUES ('CBC', 'Blood Count')
""")

# Patients
cur.execute("""
CREATE TABLE IF NOT EXISTS patients (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    age INTEGER,
    gender TEXT,
    phone TEXT
)
""")

# Visits
cur.execute("""
CREATE TABLE IF NOT EXISTS visits (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    patient_id INTEGER,
    visit_date TEXT,
    doctor_name TEXT,
    diagnosis TEXT,
    prescription TEXT,
    FOREIGN KEY(patient_id) REFERENCES patients(id)
)
""")

# Sample data
#cur.execute("""
#INSERT INTO patients (name, age, gender, phone)
#VALUES ('John Smith', 35, 'Male', '555-1234')
#""")

cur.execute("""
INSERT INTO patients (name, age, gender, phone)
VALUES ('Jenny Gardener', 25, 'Female', '361-6743')
""")

cur.execute("""
INSERT INTO visits (patient_id, visit_date, doctor_name, diagnosis, prescription)
VALUES (1, '2026-01-10', 'Dr. Sarah Ahmed', 'Flu', 'Paracetamol 500mg')
""")

con.commit()
con.close()
