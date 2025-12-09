from typing import List
from pymysql.cursors import DictCursor

from Dao.AbstractLabTechDao import LabTechDaoService
from DbConnection.ConnectionDB import ConnectionDB

from models.lab_test_order import LabTestOrder
from models.lab_result import LabResult
from models.lab_bill import LabBill


class LabTechDaoImplementation(LabTechDaoService):

    def __init__(self):
        self.conn = ConnectionDB().get_connection()

    # --------------------------------------------------
    # PENDING TESTS
    # --------------------------------------------------
    def list_pending_tests(self) -> List[LabTestOrder]:
        result = []
        cursor = None
        try:
            cursor = self.conn.cursor(DictCursor)
            cursor.execute(
                "SELECT * FROM lab_test_order WHERE status='Pending'"
            )
            for row in cursor.fetchall():
                result.append(
                    LabTestOrder(
                        lab_test_id=row["lab_test_id"],
                        appointment_id=row["appointment_id"],
                        patient_id=row["patient_id"],
                        doctor_id=row["doctor_id"],
                        token_no=row["token_no"],
                        test_name=row["test_name"],
                        notes=row["notes"],
                        status=row["status"],
                    )
                )
        except Exception as e:
            print("list_pending_tests error:", e)
        finally:
            if cursor: cursor.close()
        return result


    # --------------------------------------------------
    # COMPLETED TESTS
    # --------------------------------------------------
    def list_completed_tests(self) -> List[LabTestOrder]:
        result = []
        cursor = None
        try:
            cursor = self.conn.cursor(DictCursor)
            cursor.execute(
                "SELECT * FROM lab_test_order WHERE status='Completed'"
            )
            for row in cursor.fetchall():
                result.append(
                    LabTestOrder(
                        lab_test_id=row["lab_test_id"],
                        appointment_id=row["appointment_id"],
                        patient_id=row["patient_id"],
                        doctor_id=row["doctor_id"],
                        token_no=row["token_no"],
                        test_name=row["test_name"],
                        notes=row["notes"],
                        status=row["status"],
                    )
                )
        except Exception as e:
            print("list_completed_tests error:", e)
        finally:
            if cursor: cursor.close()
        return result


    # --------------------------------------------------
    # SAVE LAB RESULT
    # --------------------------------------------------
    def save_lab_result(self, result: LabResult) -> str:
        cursor = None
        try:
            cursor = self.conn.cursor()
            cursor.execute(
                """
                INSERT INTO lab_result
                (lab_test_id, observations, parameters, result_date)
                VALUES (%s,%s,%s,%s)
                """,
                (
                    result.get_lab_test_id(),
                    result.get_observations(),
                    result.get_parameters(),
                    result.get_result_date().strftime("%Y-%m-%d %H:%M:%S"),
                )
            )
            self.conn.commit()

            cur2 = self.conn.cursor(DictCursor)
            cur2.execute(
                """
                SELECT lab_result_id FROM lab_result
                WHERE lab_test_id=%s
                ORDER BY lab_result_id DESC LIMIT 1
                """,
                (result.get_lab_test_id(),)
            )
            row = cur2.fetchone()
            cur2.close()
            if row:
                return row["lab_result_id"]

        except Exception as e:
            print("save_lab_result error:", e)
            self.conn.rollback()
        finally:
            if cursor: cursor.close()
        return ""


    # --------------------------------------------------
    # MARK TEST AS COMPLETED
    # --------------------------------------------------
    def set_lab_test_completed(self, lab_test_id: str) -> bool:
        cursor = None
        try:
            cursor = self.conn.cursor()
            cursor.execute(
                "UPDATE lab_test_order SET status='Completed' WHERE lab_test_id=%s",
                (lab_test_id,)
            )
            self.conn.commit()
            return cursor.rowcount == 1
        except Exception as e:
            print("set_lab_test_completed error:", e)
            self.conn.rollback()
        finally:
            if cursor: cursor.close()
        return False


    # --------------------------------------------------
    # GENERATE LAB BILL
    # --------------------------------------------------
    def generate_lab_bill(self, lab_bill: LabBill) -> str:
        cursor = None
        try:
            cursor = self.conn.cursor()
            cursor.execute(
                """
                INSERT INTO lab_bill
                (lab_test_id, patient_id, total_amount, status, generated_date)
                VALUES (%s,%s,%s,%s,%s)
                """,
                (
                    lab_bill.get_lab_test_id(),
                    lab_bill.get_patient_id(),
                    lab_bill.get_total_amount(),
                    lab_bill.get_status(),
                    lab_bill.get_generated_date().strftime("%Y-%m-%d %H:%M:%S"),
                )
            )
            self.conn.commit()

            cur2 = self.conn.cursor(DictCursor)
            cur2.execute(
                """
                SELECT lab_bill_id FROM lab_bill
                WHERE lab_test_id=%s
                ORDER BY lab_bill_id DESC LIMIT 1
                """,
                (lab_bill.get_lab_test_id(),)
            )
            row = cur2.fetchone()
            cur2.close()
            if row:
                return row["lab_bill_id"]

        except Exception as e:
            print("generate_lab_bill error:", e)
            self.conn.rollback()
        finally:
            if cursor: cursor.close()
        return ""


    # --------------------------------------------------
    # LIST LAB BILLS
    # --------------------------------------------------
    def list_lab_bills(self) -> List[LabBill]:
        result = []
        cursor = None
        try:
            cursor = self.conn.cursor(DictCursor)
            cursor.execute("SELECT * FROM lab_bill")
            for row in cursor.fetchall():
                result.append(
                    LabBill(
                        lab_bill_id=row["lab_bill_id"],
                        lab_test_id=row["lab_test_id"],     
                        patient_id=row["patient_id"],
                        total_amount=row["total_amount"],
                        status=row["status"],
                        generated_date=row["generated_date"],
                    )
                )
        except Exception as e:
            print("list_lab_bills error:", e)
        finally:
            if cursor: cursor.close()
        return result

    # --------------------------------------------------
    # CHECK LAB TEST EXISTS + RETURN ITS DETAILS
    # --------------------------------------------------
    def get_lab_test_by_id(self, lab_test_id: str):
        cursor = None
        try:
            cursor = self.conn.cursor(DictCursor)
            cursor.execute(
                "SELECT * FROM lab_test_order WHERE lab_test_id=%s",
                (lab_test_id,)
            )
            return cursor.fetchone()
        except Exception as e:
            print("get_lab_test_by_id error:", e)
            return None
        finally:
            if cursor: cursor.close()

    def get_bill_by_lab_test_id(self, lab_test_id: str):
        cursor = None
        try:
            cursor = self.conn.cursor(DictCursor)
            cursor.execute(
                """
                SELECT *
                FROM lab_bill
                WHERE lab_test_id = %s
                LIMIT 1
                """,
                (lab_test_id,)
            )
            return cursor.fetchone()
        except Exception as e:
            print("get_today_lab_bill error:", e)
            return None
        finally:
            if cursor:
                cursor.close()

