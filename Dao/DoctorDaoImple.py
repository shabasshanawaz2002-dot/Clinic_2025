from typing import List
from pymysql.cursors import DictCursor

from Dao.AbstractDoctorDao import DoctorDaoService
from DbConnection.ConnectionDB import ConnectionDB

from models.appointment import Appointment
from models.prescription import Prescription
from models.lab_test_order import LabTestOrder


class DoctorDaoImplementation(DoctorDaoService):

    def __init__(self):
        self.conn = ConnectionDB().get_connection()

    # -------------------------------------------------------
    # GET TODAY APPOINTMENTS OF A DOCTOR
    # -------------------------------------------------------

    def list_today_appointments(self, doctor_id: str) -> List[Appointment]:
        result = []
        cursor = None
        try:
            cursor = self.conn.cursor(DictCursor)
            cursor.execute(
                """
                SELECT a.*, p.name AS patient_name
                FROM appointment a
                JOIN patient p ON a.patient_id = p.patient_id
                WHERE a.doctor_id=%s 
                AND DATE(a.appointment_date)=CURDATE()
                ORDER BY a.token_no
                """,
                (doctor_id,)
            )
            for row in cursor.fetchall():
                appt = Appointment(
                    appointment_id=row["appointment_id"],
                    patient_id=row["patient_id"],
                    doctor_id=row["doctor_id"],
                    appointment_date=row["appointment_date"],    # DATE
                    appointment_time=row["appointment_time"],    # TIME
                    token_no=row["token_no"],
                    status=row["status"],
                )
                
                # NEW: add patient name dynamically
                appt.patient_name = row["patient_name"]

                result.append(appt)

        except Exception as e:
            print("List doctor appointments error:", e)
        finally:
            if cursor: cursor.close()

        return result


    # -------------------------------------------------------
    # SAVE PRESCRIPTION
    # -------------------------------------------------------
    def save_prescription(self, prescription: Prescription) -> str:
        cursor = None
        try:
            cursor = self.conn.cursor()
            cursor.execute(
                """
                INSERT INTO prescription
                (appointment_id, patient_id, doctor_id, token_no,
                 symptoms, diagnosis, medication, dosage, duration, notes,
                 created_at)
                VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
                """,
                (
                    prescription.get_appointment_id(),
                    prescription.get_patient_id(),
                    prescription.get_doctor_id(),
                    prescription.get_token_no(),
                    prescription.get_symptoms(),
                    prescription.get_diagnosis(),
                    prescription.get_medication(),
                    prescription.get_dosage(),
                    prescription.get_duration(),
                    prescription.get_notes(),
                    prescription.get_created_at().strftime("%Y-%m-%d %H:%M:%S"),
                )
            )
            self.conn.commit()

            cur2 = self.conn.cursor(DictCursor)
            cur2.execute(
                """
                SELECT prescription_id FROM prescription
                WHERE appointment_id=%s
                ORDER BY prescription_id DESC LIMIT 1
                """,
                (prescription.get_appointment_id(),)
            )
            row = cur2.fetchone()
            cur2.close()
            if row:
                return row["prescription_id"]

        except Exception as e:
            print("Save prescription error:", e)
            self.conn.rollback()
        finally:
            if cursor: cursor.close()

        return ""

    # -------------------------------------------------------
    # UPDATE APPOINTMENT STATUS
    # -------------------------------------------------------
    def update_appointment_status(self, appointment_id: str, status: str) -> bool:
        cursor = None
        try:
            cursor = self.conn.cursor()
            cursor.execute(
                "UPDATE appointment SET status=%s WHERE appointment_id=%s",
                (status, appointment_id)
            )
            self.conn.commit()
            return cursor.rowcount == 1
        except Exception as e:
            print("Update appointment status error:", e)
            self.conn.rollback()
        finally:
            if cursor: cursor.close()
        return False

    # -------------------------------------------------------
    # REQUEST LAB TEST
    # -------------------------------------------------------
    def request_lab_test(self, order: LabTestOrder) -> str:
        cursor = None
        try:
            cursor = self.conn.cursor()
            cursor.execute(
                """
                INSERT INTO lab_test_order
                (appointment_id, patient_id, doctor_id, token_no,
                 test_name, notes, status)
                VALUES (%s,%s,%s,%s,%s,%s,%s)
                """,
                (
                    order.get_appointment_id(),
                    order.get_patient_id(),
                    order.get_doctor_id(),
                    order.get_token_no(),
                    order.get_test_name(),
                    order.get_notes(),
                    order.get_status(),
                )
            )
            self.conn.commit()

            cur2 = self.conn.cursor(DictCursor)
            cur2.execute(
                """
                SELECT lab_test_id FROM lab_test_order 
                WHERE appointment_id=%s
                ORDER BY lab_test_id DESC LIMIT 1
                """,
                (order.get_appointment_id(),)
            )
            row = cur2.fetchone()
            cur2.close()
            if row:
                return row["lab_test_id"]

        except Exception as e:
            print("Request lab test error:", e)
            self.conn.rollback()
        finally:
            if cursor: cursor.close()
        return ""

    # -------------------------------------------------------
    # VIEW PATIENT HISTORY (ALL PRESCRIPTIONS)
    # -------------------------------------------------------
    def view_patient_history(self, patient_id: str) -> List[Prescription]:
        result = []
        cursor = None
        try:
            cursor = self.conn.cursor(DictCursor)
            cursor.execute(
                """
                SELECT * FROM prescription
                WHERE patient_id=%s
                ORDER BY created_at DESC
                """,
                (patient_id,)
            )
            for row in cursor.fetchall():
                result.append(
                    Prescription(
                        prescription_id=row["prescription_id"],
                        appointment_id=row["appointment_id"],
                        patient_id=row["patient_id"],
                        doctor_id=row["doctor_id"],
                        token_no=row["token_no"],
                        symptoms=row["symptoms"],
                        diagnosis=row["diagnosis"],
                        medication=row["medication"],
                        dosage=row["dosage"],
                        duration=row["duration"],
                        notes=row["notes"],
                        created_at=row["created_at"],       # DATETIME returned by MySQL
                    )
                )
        except Exception as e:
            print("View patient history error:", e)
        finally:
            if cursor: cursor.close()

        return result
