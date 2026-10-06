import sqlite3
import json
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
POSSIBLE_CLINIC_PATHS = [
    os.path.join(BASE_DIR, "clinic.json"),
    os.path.join(os.path.dirname(os.path.abspath(__file__)), "clinic.json"),
    os.path.join(os.getcwd(), "clinic.json"),
    os.path.join(os.getcwd(), "backend", "clinic.json")
]

def load_clinic_data():
    for path in POSSIBLE_CLINIC_PATHS:
        if os.path.exists(path):
            with open(path, "r", encoding="utf-8") as f:
                return json.load(f)
    raise FileNotFoundError(f"clinic.json not found in any of: {POSSIBLE_CLINIC_PATHS}")

CLINIC_DATA = load_clinic_data()

def create_db():
    """Creates a new isolated in-memory SQLite database populated with clinic.json data."""
    conn = sqlite3.connect(":memory:")
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    cursor.execute('''
        CREATE TABLE clinic (
            id TEXT PRIMARY KEY,
            name TEXT,
            city TEXT,
            timezone TEXT,
            slot_minutes INTEGER,
            reference_date TEXT
        )
    ''')
    cursor.execute('''
        CREATE TABLE doctors (
            id TEXT PRIMARY KEY,
            name TEXT,
            speciality TEXT
        )
    ''')
    cursor.execute('''
        CREATE TABLE doctor_windows (
            doctor_id TEXT,
            day TEXT,
            start TEXT,
            end TEXT,
            FOREIGN KEY(doctor_id) REFERENCES doctors(id)
        )
    ''')
    cursor.execute('''
        CREATE TABLE doctor_leaves (
            doctor_id TEXT,
            date TEXT,
            FOREIGN KEY(doctor_id) REFERENCES doctors(id)
        )
    ''')
    cursor.execute('''
        CREATE TABLE holidays (
            date TEXT PRIMARY KEY
        )
    ''')
    cursor.execute('''
        CREATE TABLE patients (
            id TEXT PRIMARY KEY,
            name TEXT,
            phone TEXT,
            dob TEXT
        )
    ''')
    cursor.execute('''
        CREATE TABLE patient_guardians (
            guardian_id TEXT,
            ward_id TEXT,
            FOREIGN KEY(guardian_id) REFERENCES patients(id),
            FOREIGN KEY(ward_id) REFERENCES patients(id)
        )
    ''')
    cursor.execute('''
        CREATE TABLE appointments (
            id TEXT PRIMARY KEY,
            patient_id TEXT,
            doctor_id TEXT,
            date TEXT,
            start TEXT,
            end TEXT,
            status TEXT,
            FOREIGN KEY(patient_id) REFERENCES patients(id),
            FOREIGN KEY(doctor_id) REFERENCES doctors(id)
        )
    ''')

    c = CLINIC_DATA["clinic"]
    cursor.execute('INSERT INTO clinic VALUES (?, ?, ?, ?, ?, ?)', 
                   (c["id"], c["name"], c["city"], c["timezone"], c["slot_minutes"], c["reference_date"]))

    for doc in CLINIC_DATA["doctors"]:
        cursor.execute('INSERT INTO doctors VALUES (?, ?, ?)', (doc["id"], doc["name"], doc["speciality"]))
        for w in doc["windows"]:
            cursor.execute('INSERT INTO doctor_windows VALUES (?, ?, ?, ?)', (doc["id"], w["day"], w["start"], w["end"]))
        for d in doc.get("leave_dates", []):
            cursor.execute('INSERT INTO doctor_leaves VALUES (?, ?)', (doc["id"], d))

    for h in CLINIC_DATA["holidays"]:
        cursor.execute('INSERT INTO holidays VALUES (?)', (h,))

    for p in CLINIC_DATA["patients"]:
        cursor.execute('INSERT INTO patients VALUES (?, ?, ?, ?)', (p["id"], p["name"], p["phone"], p["dob"]))
        for w in p.get("guardian_of", []):
            cursor.execute('INSERT INTO patient_guardians VALUES (?, ?)', (p["id"], w))

    for a in CLINIC_DATA["appointments"]:
        cursor.execute('INSERT INTO appointments VALUES (?, ?, ?, ?, ?, ?, ?)',
                       (a["id"], a["patient_id"], a["doctor_id"], a["date"], a["start"], a["end"], a["status"]))
    
    conn.commit()
    return conn
