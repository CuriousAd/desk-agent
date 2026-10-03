import sqlite3
import uuid
from datetime import datetime

def hm_to_mins(hm: str) -> int:
    h, m = map(int, hm.split(':'))
    return h * 60 + m

def mins_to_hm(mins: int) -> str:
    return f"{mins // 60:02d}:{mins % 60:02d}"

def get_day_of_week(date_str: str) -> str:
    dt = datetime.strptime(date_str, "%Y-%m-%d")
    days = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
    return days[dt.weekday()]

def search_slots(conn: sqlite3.Connection, doctor_id: str, date: str):
    cursor = conn.cursor()
    cursor.execute("SELECT 1 FROM holidays WHERE date = ?", (date,))
    if cursor.fetchone():
        return {"slots": [], "message": f"{date} is a clinic holiday."}
    
    cursor.execute("SELECT 1 FROM doctor_leaves WHERE doctor_id = ? AND date = ?", (doctor_id, date))
    if cursor.fetchone():
        return {"slots": [], "message": f"Doctor {doctor_id} is on leave on {date}."}
        
    day = get_day_of_week(date)
    cursor.execute("SELECT start, end FROM doctor_windows WHERE doctor_id = ? AND day = ?", (doctor_id, day))
    windows = cursor.fetchall()
    
    if not windows:
        return {"slots": [], "message": f"Doctor {doctor_id} does not work on {day}."}
        
    cursor.execute("SELECT slot_minutes FROM clinic LIMIT 1")
    slot_minutes = cursor.fetchone()["slot_minutes"]
    
    all_slots = []
    for w in windows:
        start_m = hm_to_mins(w["start"])
        end_m = hm_to_mins(w["end"])
        curr_m = start_m
        while curr_m + slot_minutes <= end_m:
            all_slots.append(mins_to_hm(curr_m))
            curr_m += slot_minutes
            
    cursor.execute("SELECT start FROM appointments WHERE doctor_id = ? AND date = ? AND status = 'booked'", (doctor_id, date))
    booked_starts = {row["start"] for row in cursor.fetchall()}
    
    free_slots = [s for s in all_slots if s not in booked_starts]
    return {"slots": free_slots}

def book_appointment(conn: sqlite3.Connection, patient_id: str, doctor_id: str, date: str, start: str):
    cursor = conn.cursor()
    cursor.execute("SELECT 1 FROM patients WHERE id = ?", (patient_id,))
    if not cursor.fetchone():
        return {"status": "error", "message": f"Patient {patient_id} not found."}
        
    cursor.execute("SELECT 1 FROM doctors WHERE id = ?", (doctor_id,))
    if not cursor.fetchone():
        return {"status": "error", "message": f"Doctor {doctor_id} not found."}
        
    slots_resp = search_slots(conn, doctor_id, date)
    if "slots" not in slots_resp or start not in slots_resp["slots"]:
        return {"status": "error", "message": f"Slot {start} on {date} is not available or doctor is unavailable."}
        
    cursor.execute("SELECT slot_minutes FROM clinic LIMIT 1")
    slot_minutes = cursor.fetchone()["slot_minutes"]
    end = mins_to_hm(hm_to_mins(start) + slot_minutes)
    app_id = f"ap_{uuid.uuid4().hex[:8]}"
    
    try:
        # Prevent double booking race condition
        cursor.execute("SELECT 1 FROM appointments WHERE doctor_id = ? AND date = ? AND start = ? AND status = 'booked'", (doctor_id, date, start))
        if cursor.fetchone():
            return {"status": "error", "message": f"Slot {start} on {date} was just booked by someone else."}
            
        cursor.execute("INSERT INTO appointments (id, patient_id, doctor_id, date, start, end, status) VALUES (?, ?, ?, ?, ?, ?, ?)",
                       (app_id, patient_id, doctor_id, date, start, end, "booked"))
        conn.commit()
        return {"status": "success", "appointment_id": app_id, "message": "Appointment booked successfully."}
    except Exception as e:
        conn.rollback()
        return {"status": "error", "message": str(e)}

def cancel_appointment(conn: sqlite3.Connection, appointment_id: str):
    cursor = conn.cursor()
    cursor.execute("SELECT status FROM appointments WHERE id = ?", (appointment_id,))
    row = cursor.fetchone()
    if not row:
        return {"status": "error", "message": f"Appointment {appointment_id} not found."}
    if row["status"] == "cancelled":
        return {"status": "error", "message": f"Appointment {appointment_id} is already cancelled."}
        
    cursor.execute("UPDATE appointments SET status = 'cancelled' WHERE id = ?", (appointment_id,))
    conn.commit()
    return {"status": "success", "message": "Appointment cancelled successfully."}

def reschedule_appointment(conn: sqlite3.Connection, appointment_id: str, new_date: str, new_start: str):
    cursor = conn.cursor()
    cursor.execute("SELECT patient_id, doctor_id, status FROM appointments WHERE id = ?", (appointment_id,))
    row = cursor.fetchone()
    if not row:
        return {"status": "error", "message": f"Appointment {appointment_id} not found."}
    if row["status"] == "cancelled":
        return {"status": "error", "message": "Cannot reschedule a cancelled appointment."}
        
    doctor_id = row["doctor_id"]
    
    slots_resp = search_slots(conn, doctor_id, new_date)
    if "slots" not in slots_resp or new_start not in slots_resp["slots"]:
        return {"status": "error", "message": f"Slot {new_start} on {new_date} is not available."}
        
    cursor.execute("SELECT slot_minutes FROM clinic LIMIT 1")
    slot_minutes = cursor.fetchone()["slot_minutes"]
    new_end = mins_to_hm(hm_to_mins(new_start) + slot_minutes)
    
    try:
        cursor.execute("SELECT 1 FROM appointments WHERE doctor_id = ? AND date = ? AND start = ? AND status = 'booked'", (doctor_id, new_date, new_start))
        if cursor.fetchone():
            return {"status": "error", "message": f"Slot {new_start} on {new_date} was just booked by someone else."}
            
        cursor.execute("UPDATE appointments SET date = ?, start = ?, end = ? WHERE id = ?", (new_date, new_start, new_end, appointment_id))
        conn.commit()
        return {"status": "success", "message": "Appointment rescheduled successfully."}
    except Exception as e:
        conn.rollback()
        return {"status": "error", "message": str(e)}

def lookup_patient(conn: sqlite3.Connection, search_query: str):
    cursor = conn.cursor()
    search_term = f"%{search_query.lower()}%"
    cursor.execute("SELECT id, name, phone, dob FROM patients WHERE LOWER(name) LIKE ? OR phone LIKE ?", (search_term, search_term))
    rows = cursor.fetchall()
    
    candidates = []
    for r in rows:
        cursor.execute("SELECT ward_id FROM patient_guardians WHERE guardian_id = ?", (r["id"],))
        wards = [w["ward_id"] for w in cursor.fetchall()]
        candidates.append({
            "id": r["id"],
            "name": r["name"],
            "phone": r["phone"],
            "dob": r["dob"],
            "guardian_of": wards
        })
    return {"candidates": candidates}

def escalate_to_human(reason: str, detail: str = ""):
    return {"status": "escalated", "reason": reason, "detail": detail}
