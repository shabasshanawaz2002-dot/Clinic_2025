from typing import List, Optional
from pymysql.cursors import DictCursor

from Dao.AbstractAdminDao import AdminDaoService
from DbConnection.ConnectionDB import ConnectionDB
from models.staff import Staff
from models.doctor import Doctor


class AdminDaoImplementation(AdminDaoService):

    def _init_(self):
        self.conn = ConnectionDB().get_connection()


    # ------------------------------------------------
    # LOGIN
    # ------------------------------------------------
    def authenticate_staff(self, username: str, password: str) -> Optional[Staff]:
        cursor = None
        try:
            cursor = self.conn.cursor(DictCursor)
            cursor.execute(
                """
                SELECT * FROM staff 
                WHERE username=%s AND password=%s AND status='Active'
                """,
                (username, password),
            )
            row = cursor.fetchone()
            if row:
                return Staff(
                    staff_id=row["staff_id"],
                    name=row["name"],
                    phone=row["phone"],
                    address=row["address"],
                    age=row["age"],
                    gender=row["gender"],
                    email=row["email"],
                    role=row["role"],
                    username=row["username"],
                    password=row["password"],
                    qualifications=row["qualifications"],
                    date_of_joining=row["date_of_joining"],  # PyMySQL gives datetime.date already
                    salary=row["salary"],
                    status=row["status"],
                )
        except Exception as e:
            print("Login error:", e)
        finally:
            if cursor: cursor.close()
        return None


    # ------------------------------------------------
    # ADD STAFF
    # ------------------------------------------------
    def add_staff(self, staff: Staff) -> str:
        cursor = None
        try:
            cursor = self.conn.cursor()
            cursor.execute(
                """
                INSERT INTO staff
                (name, phone, address, age, gender, email, role, username, password,
                 qualifications, date_of_joining, salary, status)
                VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
                """,
                (
                    staff.get_name(),
                    staff.get_phone(),
                    staff.get_address(),
                    staff.get_age(),
                    staff.get_gender(),
                    staff.get_email(),
                    staff.get_role(),
                    staff.get_username(),
                    staff.get_password(),
                    staff.get_qualifications(),
                    staff.get_date_of_joining().strftime("%Y-%m-%d"), # <-- DATETIME FIX
                    staff.get_salary(),
                    staff.get_status(),
                ),
            )
            self.conn.commit()

            cursor2 = self.conn.cursor(DictCursor)
            cursor2.execute(
                "SELECT staff_id FROM staff WHERE username=%s ORDER BY staff_id DESC LIMIT 1",
                (staff.get_username(),),
            )
            row = cursor2.fetchone()
            cursor2.close()
            if row:
                return row["staff_id"]
        except Exception as e:
            print("Add staff error:", e)
            self.conn.rollback()
        finally:
            if cursor: cursor.close()
        return ""


    # ------------------------------------------------
    # SEARCH STAFF
    # ------------------------------------------------
    def search_staff_by_id(self, staff_id: str) -> Optional[Staff]:
        cursor = None
        try:
            cursor = self.conn.cursor(DictCursor)
            cursor.execute("SELECT * FROM staff WHERE staff_id=%s", (staff_id,))
            row = cursor.fetchone()
            if row:
                return Staff(
                    staff_id=row["staff_id"],
                    name=row["name"],
                    phone=row["phone"],
                    address=row["address"],
                    age=row["age"],
                    gender=row["gender"],
                    email=row["email"],
                    role=row["role"],
                    username=row["username"],
                    password=row["password"],
                    qualifications=row["qualifications"],
                    date_of_joining=row["date_of_joining"],
                    salary=row["salary"],
                    status=row["status"],
                )
        except Exception as e:
            print("Search staff error:", e)
        finally:
            if cursor: cursor.close()
        return None

    def search_staff_by_phone(self, phone: str) -> Optional[Staff]:
        cursor = None
        try:
            cursor = self.conn.cursor(DictCursor)
            cursor.execute("SELECT * FROM staff WHERE phone=%s", (phone,))
            row = cursor.fetchone()
            if row:
                return Staff(
                    staff_id=row["staff_id"],
                    name=row["name"],
                    phone=row["phone"],
                    address=row["address"],
                    age=row["age"],
                    gender=row["gender"],
                    email=row["email"],
                    role=row["role"],
                    username=row["username"],
                    password=row["password"],
                    qualifications=row["qualifications"],
                    date_of_joining=row["date_of_joining"],
                    salary=row["salary"],
                    status=row["status"],
                )
        except Exception as e:
            print("Search staff error:", e)
        finally:
            if cursor: cursor.close()
        return None

    # ------------------------------------------------
    # LIST STAFF
    # ------------------------------------------------
    def list_all_staff(self) -> List[Staff]:
        result: List[Staff] = []
        cursor = None
        try:
            cursor = self.conn.cursor(DictCursor)
            cursor.execute("SELECT * FROM staff")
            for row in cursor.fetchall():
                result.append(
                    Staff(
                        staff_id=row["staff_id"],
                        name=row["name"],
                        phone=row["phone"],
                        address=row["address"],
                        age=row["age"],
                        gender=row["gender"],
                        email=row["email"],
                        role=row["role"],
                        username=row["username"],
                        password=row["password"],
                        qualifications=row["qualifications"],
                        date_of_joining=row["date_of_joining"],
                        salary=row["salary"],
                        status=row["status"],
                    )
                )
        except Exception as e:
            print("List staff error:", e)
        finally:
            if cursor: cursor.close()
        return result


    # ------------------------------------------------
    # UPDATE STAFF
    # ------------------------------------------------
    def update_staff(self, staff: Staff) -> bool:
        cursor = None
        try:
            cursor = self.conn.cursor()
            cursor.execute(
                """
                UPDATE staff
                SET name=%s, phone=%s, address=%s, salary=%s, status=%s
                WHERE staff_id=%s
                """,
                (
                    staff.get_name(),
                    staff.get_phone(),
                    staff.get_address(),
                    staff.get_salary(),
                    staff.get_status(),
                    staff.get_staff_id(),
                ),
            )
            self.conn.commit()
            return cursor.rowcount == 1
        except Exception as e:
            print("Update staff error:", e)
            self.conn.rollback()
        finally:
            if cursor: cursor.close()
        return False


    # ------------------------------------------------
    # DEACTIVATE STAFF
    # ------------------------------------------------
    def deactivate_staff(self, staff_id: str) -> bool:
        cursor = None
        try:
            cursor = self.conn.cursor()
            cursor.execute(
                "UPDATE staff SET status='Inactive' WHERE staff_id=%s",
                (staff_id,)
            )
            self.conn.commit()
            return cursor.rowcount == 1
        except Exception as e:
            print("Deactivate error:", e)
            self.conn.rollback()
        finally:
            if cursor: cursor.close()
        return False


    # ========================================================
    #  DOCTOR SECTION
    # ========================================================
    def add_doctor_profile(self, doctor: Doctor) -> str:
        cursor = None
        try:
            cursor = self.conn.cursor()
            cursor.execute(
                """
                INSERT INTO doctor
                (staff_id, specialization, consultation_fee, working_hours, status)
                VALUES (%s,%s,%s,%s,%s)
                """,
                (
                    doctor.get_staff_id(),
                    doctor.get_specialization(),
                    doctor.get_consultation_fee(),
                    doctor.get_working_hours(),
                    doctor.get_status(),
                ),
            )
            self.conn.commit()

            cursor2 = self.conn.cursor(DictCursor)
            cursor2.execute(
                "SELECT doctor_id FROM doctor WHERE staff_id=%s ORDER BY doctor_id DESC LIMIT 1",
                (doctor.get_staff_id(),),
            )
            row = cursor2.fetchone()
            cursor2.close()
            if row:
                return row["doctor_id"]
        except Exception as e:
            print("Add doctor error:", e)
            self.conn.rollback()
        finally:
            if cursor: cursor.close()
        return ""


    def update_doctor_profile(self, doctor: Doctor) -> bool:
        cursor = None
        try:
            cursor = self.conn.cursor()
            cursor.execute(
                """
                UPDATE doctor 
                SET specialization=%s, consultation_fee=%s, working_hours=%s, status=%s
                WHERE doctor_id=%s
                """,
                (
                    doctor.get_specialization(),
                    doctor.get_consultation_fee(),
                    doctor.get_working_hours(),
                    doctor.get_status(),
                    doctor.get_doctor_id(),
                ),
            )
            self.conn.commit()
            return cursor.rowcount == 1
        except Exception as e:
            print("Update doctor error:", e)
            self.conn.rollback()
        finally:
            if cursor: cursor.close()
        return False


    def list_all_doctors(self) -> List[Doctor]:
        result: List[Doctor] = []
        cursor = None
        try:
            cursor = self.conn.cursor(DictCursor)
            cursor.execute("SELECT * FROM doctor")
            for row in cursor.fetchall():
                result.append(
                    Doctor(
                        doctor_id=row["doctor_id"],
                        staff_id=row["staff_id"],
                        specialization=row["specialization"],
                        consultation_fee=row["consultation_fee"],
                        working_hours=row["working_hours"],
                        status=row["status"],
                    )
                )
        finally:
            if cursor: cursor.close()
        return result


    def find_doctor_by_id(self, doctor_id: str) -> Optional[Doctor]:
        cursor = None
        try:
            cursor = self.conn.cursor(DictCursor)

            query = """
                SELECT d.*, s.name, s.phone, s.salary
                FROM doctor d
                JOIN staff s ON d.staff_id = s.staff_id
                WHERE d.doctor_id = %s
            """

            cursor.execute(query, (doctor_id,))
            row = cursor.fetchone()

            if row:

                # just print details here
                print(f"Name: {row['name']}")
                print(f"Contact: {row['phone']}")

                # return original Doctor object (unchanged)
                return Doctor(
                    doctor_id=row["doctor_id"],
                    staff_id=row["staff_id"],
                    specialization=row["specialization"],
                    consultation_fee=row["consultation_fee"],
                    working_hours=row["working_hours"],
                    status=row["status"]
                )

        except Exception as e:
            print("Find doctor error:", e)
        finally:
            if cursor: cursor.close()

        return None