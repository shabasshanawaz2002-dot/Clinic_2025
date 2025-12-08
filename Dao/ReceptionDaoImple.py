from typing import List
from datetime import datetime, date

from Dao.AbstractReceptionDao import ReceptionDaoService
from DbConnection.ConnectionDB import ConnectionDB

from models.patient import Patient
from models.appointment import Appointment
from models.bill import Bill

from pymysql.cursors import DictCursor


# ================= SQL =====================

INSERT_PATIENT = """
INSERT INTO patient(name, age, blood_group, gender, phone, address, emergency_contact)
VALUES (%s, %s, %s, %s, %s, %s, %s)
"""

SEARCH_PATIENT_BY_ID = """
SELECT * FROM patient WHERE patient_id = %s
"""

SEARCH_PATIENT_BY_PHONE = """
SELECT * FROM patient WHERE phone = %s
"""

LIST_ALL_PATIENT = """
SELECT * FROM patient
"""

GET_DOCTOR_BY_ID = """
SELECT * FROM doctor WHERE doctor_id = %s
"""

GET_MAX_TOKEN = """
SELECT MAX(token_no) AS max_token
FROM appointment
WHERE doctor_id = %s AND appointment_date = %s
"""

INSERT_APPOINTMENT = """
INSERT INTO appointment(patient_id, doctor_id, appointment_date, appointment_time, token_no, status)
VALUES (%s, %s, %s, %s, %s, %s)
"""

GET_LAST_APPOINTMENT_ID = """
SELECT appointment_id 
FROM appointment
WHERE patient_id = %s AND doctor_id = %s AND appointment_date = %s AND appointment_time = %s
ORDER BY appointment_id DESC
LIMIT 1
"""

LIST_TODAY_APPOINTMENTS = """
SELECT * FROM appointment WHERE appointment_date = %s ORDER BY appointment_time
"""

LIST_TODAY_APPOINTMENTS_BY_DOCTOR = """
SELECT * FROM appointment
WHERE appointment_date = %s AND doctor_id = %s
ORDER BY appointment_time
"""

CANCEL_APPOINTMENT = """
UPDATE appointment SET status = 'Cancelled' WHERE appointment_id = %s
"""

INSERT_BILL = """
INSERT INTO bill(appointment_id, patient_id, doctor_id, amount, generated_date, status)
VALUES (%s,%s,%s,%s,%s,%s)
"""

LIST_CONSULTATION_BILLS = """
SELECT * FROM bill ORDER BY generated_date DESC
"""

CHECK_TIME_EXISTS = """
SELECT appointment_id FROM appointment
WHERE doctor_id=%s AND appointment_date=%s AND appointment_time=%s
"""



# ================= IMPLEMENTATION =======================

class ReceptionDaoImplementation(ReceptionDaoService):

    def _init_(self):
        self.conn = ConnectionDB().get_connection()


    # ----------------------------------------------------
    # Add patient  (TRIGGER BASED RETURN FIX)
    # ----------------------------------------------------
    def add_patient(self, patient: Patient):
        cursor = None
        try:
            cursor = self.conn.cursor()
            cursor.execute(
                INSERT_PATIENT,
                (
                    patient.get_name(),
                    patient.get_age(),
                    patient.get_blood_group(),
                    patient.get_gender(),
                    patient.get_phone(),
                    patient.get_address(),
                    patient.get_emergency_contact()
                )
            )
            self.conn.commit()
        except Exception as e:
            print("Error inserting patient:", e)
            return None
        finally:
            if cursor:
                cursor.close()

        # fetch the generated patient_id by phone
        try:
            cursor2 = self.conn.cursor(DictCursor)
            cursor2.execute(
                "SELECT patient_id FROM patient WHERE phone=%s ORDER BY patient_id DESC LIMIT 1",
                (patient.get_phone(),)
            )
            row = cursor2.fetchone()
            cursor2.close()

            if row:
                return row["patient_id"]
            return None
        except:
            return None


    # ----------------------------------------------------
    # Search by ID
    # ----------------------------------------------------
    def search_patient_by_id(self, patient_id: str):
        cursor = None
        try:
            cursor = self.conn.cursor(DictCursor)
            cursor.execute(SEARCH_PATIENT_BY_ID, patient_id)
            row = cursor.fetchone()
            if not row:
                return None

            return Patient(
                name=row["name"],
                age=row["age"],
                blood_group=row["blood_group"],
                gender=row["gender"],
                phone=row["phone"],
                address=row["address"],
                emergency_contact=row["emergency_contact"],
                patient_id=row["patient_id"]
            )

        except Exception as e:
            print("Error searching patient:", e)
        finally:
            if cursor:
                cursor.close()


    # ----------------------------------------------------
    # Search by phone
    # ----------------------------------------------------
    def search_patient_by_phone(self, phone: str):
        cursor = None
        try:
            cursor = self.conn.cursor(DictCursor)
            cursor.execute(SEARCH_PATIENT_BY_PHONE, phone)
            row = cursor.fetchone()
            if not row:
                return None

            return Patient(
                name=row["name"],
                age=row["age"],
                blood_group=row["blood_group"],
                gender=row["gender"],
                phone=row["phone"],
                address=row["address"],
                emergency_contact=row["emergency_contact"],
                patient_id=row["patient_id"]
            )

        except Exception as e:
            print("Error searching by phone:", e)
        finally:
            if cursor:
                cursor.close()


    # ----------------------------------------------------
    # List all patients
    # ----------------------------------------------------
    def list_all_patients(self)-> List[Patient]:
        cursor = None
        pts = []
        try:
            cursor = self.conn.cursor(DictCursor)
            cursor.execute(LIST_ALL_PATIENT)
            rows = cursor.fetchall()
            for row in rows:
                pts.append(Patient(
                    name=row["name"],
                    age=row["age"],
                    blood_group=row["blood_group"],
                    gender=row["gender"],
                    phone=row["phone"],
                    address=row["address"],
                    emergency_contact=row["emergency_contact"],
                    patient_id=row["patient_id"]
                ))
            return pts

        except Exception as e:
            print("Error listing patients:", e)
            return pts
        finally:
            if cursor:
                cursor.close()


    # ----------------------------------------------------
    # Get doctor
    # ----------------------------------------------------
    def get_doctor_by_id(self, doctor_id: str):
        cursor = None
        try:
            cursor = self.conn.cursor(DictCursor)
            cursor.execute(GET_DOCTOR_BY_ID, doctor_id)
            return cursor.fetchone()
        except:
            return None
        finally:
            if cursor:
                cursor.close()


    # ----------------------------------------------------
    # Create Appointment  (TRIGGER RETURN + TOKEN FIXED)
    # ----------------------------------------------------
    def create_appointment(self, appointment: Appointment):
        cursor = None
        try:
            cursor = self.conn.cursor(DictCursor)

            appt_date = appointment.get_appointment_date()
            appt_time = appointment.get_appointment_time()

            # ---------------------------------------------------
            # NEW LOGIC (DON’T ALLOW SAME TIME FOR SAME DOCTOR)
            # ---------------------------------------------------
            cursor.execute(
                CHECK_TIME_EXISTS,
                (
                    appointment.get_doctor_id(),
                    appt_date,
                    appt_time
                )
            )
            existing = cursor.fetchone()
            if existing:
                print("Time slot already booked for this doctor. Choose a different time.")
                return None
            # ---------------------------------------------------

            # ---------------------------------------------------
            # TOKEN LOGIC (RESET PER DAY, PER DOCTOR)
            # ---------------------------------------------------
            date_str = appt_date.strftime("%Y-%m-%d")

            cursor.execute(GET_MAX_TOKEN, (appointment.get_doctor_id(), date_str))
            row = cursor.fetchone()

            next_token = int(row["max_token"]) + 1 if (row and row["max_token"]) else 1

            appointment.set_token_no(str(next_token))
            # ---------------------------------------------------

            cursor.execute(
                INSERT_APPOINTMENT,
                (
                    appointment.get_patient_id(),
                    appointment.get_doctor_id(),
                    appt_date.strftime("%Y-%m-%d"),
                    appt_time.strftime("%H:%M:%S"),
                    appointment.get_token_no(),
                    appointment.get_status()
                )
            )
            self.conn.commit()

        except Exception as e:
            print("Error creating appointment:", e)
            return None
        finally:
            if cursor:
                cursor.close()

        # read real trigger value:
        try:
            cursor2 = self.conn.cursor(DictCursor)
            cursor2.execute(
                GET_LAST_APPOINTMENT_ID,
                (
                    appointment.get_patient_id(),
                    appointment.get_doctor_id(),
                    appt_date.strftime("%Y-%m-%d"),
                    appt_time.strftime("%H:%M:%S")
                )
            )
            row2 = cursor2.fetchone()
            cursor2.close()
            if row2:
                return row2["appointment_id"]
            return None

        except:
            return None

    # ----------------------------------------------------
    # List today's appointments
    # ----------------------------------------------------
    def list_today_appointments(self)-> List[Appointment]:
        cursor = None
        appts = []
        try:
            cursor = self.conn.cursor(DictCursor)
            today = date.today()
            cursor.execute(LIST_TODAY_APPOINTMENTS, today)
            rows = cursor.fetchall()

            for row in rows:
                appts.append(Appointment(
                    appointment_id=row["appointment_id"],
                    patient_id=row["patient_id"],
                    doctor_id=row["doctor_id"],
                    appointment_date=row["appointment_date"],
                    appointment_time=row["appointment_time"],
                    token_no=row["token_no"],
                    status=row["status"]
                ))

            return appts

        except Exception as e:
            print("Error listing appointments:", e)
            return appts
        finally:
            if cursor:
                cursor.close()


    # ----------------------------------------------------
    # Cancel appointment
    # ----------------------------------------------------
    def cancel_appointment(self, appointment_id: str)-> bool:
        cursor = None
        try:
            cursor = self.conn.cursor()
            cursor.execute(CANCEL_APPOINTMENT, appointment_id)
            self.conn.commit()
            return cursor.rowcount == 1
        except Exception as e:
            print("Error cancelling appointment:", e)
            return False
        finally:
            if cursor:
                cursor.close()


    # ----------------------------------------------------
    # Generate Consultation Bill  (TRIGGER RETURN)
    # ----------------------------------------------------
    def generate_consultation_bill(self, bill: Bill):
        cursor = None
        try:
            cursor = self.conn.cursor()
            cursor.execute(
                INSERT_BILL,
                (
                    bill.get_appointment_id(),
                    bill.get_patient_id(),
                    bill.get_doctor_id(),
                    bill.get_amount(),
                    bill.get_generated_date().strftime("%Y-%m-%d %H:%M:%S"),
                    bill.get_status()
                )
            )
            self.conn.commit()
        except Exception as e:
            print("Error creating bill:", e)
            return None
        finally:
            if cursor:
                cursor.close()

        # return trigger-generated bill_id
        try:
            cursor2 = self.conn.cursor(DictCursor)
            cursor2.execute(
                "SELECT bill_id FROM bill WHERE appointment_id=%s ORDER BY bill_id DESC LIMIT 1",
                (bill.get_appointment_id(),)
            )
            row = cursor2.fetchone()
            cursor2.close()
            if row:
                return row["bill_id"]
            return None

        except:
            return None


    # ----------------------------------------------------
    # List bills
    # ----------------------------------------------------
    def list_consultation_bills(self)-> List[Bill]:
        cursor = None
        bills = []
        try:
            cursor = self.conn.cursor(DictCursor)
            cursor.execute(LIST_CONSULTATION_BILLS)
            rows = cursor.fetchall()

            for row in rows:
                bills.append(Bill(
                    appointment_id=row["appointment_id"],
                    patient_id=row["patient_id"],
                    doctor_id=row["doctor_id"],
                    amount=row["amount"],
                    generated_date=row["generated_date"],
                    status=row["status"],
                    bill_id=row["bill_id"]
                ))
            return bills

        except Exception as e:
            print("Error listing bills:", e)
            return bills
        finally:
            if cursor:
                cursor.close()

# ----------------------------------------------------
    # Get appointment by ID
    # ----------------------------------------------------
    def get_appointment_by_id(self, appointment_id: str):
        cursor = None
        try:
            cursor = self.conn.cursor(DictCursor)
            cursor.execute(
                "SELECT * FROM appointment WHERE appointment_id=%s",
                (appointment_id,)
            )
            return cursor.fetchone()
        except:
            return None
        finally:
            if cursor:
                cursor.close()