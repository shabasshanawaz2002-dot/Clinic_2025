from Dao.AdminDaoImple import AdminDaoImplementation

from lib.AdminManagementLib import AdminManagementLib
from lib.ReceptionManagementLib import ReceptionManagementLib
from lib.DoctorManagementLib import DoctorManagementLib
from lib.LabManagementLib import LabManagementLib


# DAO used for Login
admin_dao = AdminDaoImplementation()


# ---------------------------------------------------------
# LOGIN
# ---------------------------------------------------------
def login():
    print("\n====== CLINICAL MANAGEMENT SYSTEM LOGIN ======")
    username = input("Username: ")
    password = input("Password: ")

    staff = admin_dao.authenticate_staff(username, password)
    if staff:
        print(f"\nLogin Successful. Welcome {staff.get_name()}")
        return staff
    else:
        print("Invalid login")
        return None


# ---------------------------------------------------------
# ADMIN MENU
# ---------------------------------------------------------
def admin_menu():
    while True:
        print("\n========== ADMIN MENU ==========")
        print("""
        ------ STAFF MANAGEMENT ------
        1. Add Staff
        2. Search Staff By ID
        3. Search Staff By Phone
        4. List Staff
        5. Update Staff
        6. Deactivate Staff

        ------ DOCTOR MANAGEMENT ------
        7. Add Doctor Profile
        8. Search Doctor By ID
        9. Update Doctor Profile
        10. List Doctors

        11. Logout
        """)

        valid = ["1","2","3","4","5","6","7","8","9","10","11"]

        while True:
            c = input("Enter choice: ")
            if c in valid:
                break
            print("Invalid choice, enter again.")

        if c == "1": AdminManagementLib.add_staff()
        elif c == "2": AdminManagementLib.search_staff()
        elif c == "3": AdminManagementLib.search_staff_by_phone()
        elif c == "4": AdminManagementLib.list_staff()
        elif c == "5": AdminManagementLib.update_staff()
        elif c == "6": AdminManagementLib.deactivate_staff()
        elif c == "7": AdminManagementLib.add_doctor()
        elif c == "8": AdminManagementLib.search_doctor_by_id()
        elif c == "9": AdminManagementLib.update_doctor()
        elif c == "10": AdminManagementLib.list_doctors()
        elif c == "11": 
            break

# ---------------------------------------------------------
# RECEPTION MENU
# ---------------------------------------------------------
def reception_menu():
    while True:
        print("\n========== RECEPTION MENU ==========")
        print("""
        ------ PATIENT MANAGEMENT ------
        1. Register Patient
        2. Search Patient By ID
        3. Search Patient By Phone
        4. List Patients

        ------ APPOINTMENT MANAGEMENT ------
        5. Create Appointment
        6. List Today's Appointments
        7. Cancel Appointment

        ------ BILLING ------
        8. Generate Consultation Bill
        9. List Consultation Bills

        10. Logout
        """)

        valid = ["1","2","3","4","5","6","7","8","9","10"]

        while True:
            c = input("Enter choice: ")
            if c in valid:
                break
            print("Invalid choice, please enter again.")

        # PATIENT
        if c == "1": ReceptionManagementLib.add_patient()
        elif c == "2": ReceptionManagementLib.search_patient()
        elif c == "3": ReceptionManagementLib.search_patient_by_phone()
        elif c == "4": ReceptionManagementLib.list_patients()

        # APPOINTMENT
        elif c == "5": ReceptionManagementLib.create_appointment()
        elif c == "6": ReceptionManagementLib.list_todays_appointments()
        elif c == "7": ReceptionManagementLib.cancel_appointment()

        # BILLING
        elif c == "8": ReceptionManagementLib.generate_consultation_bill()
        elif c == "9": ReceptionManagementLib.list_consultation_bills()

        elif c == "10":
            break

# ---------------------------------------------------------
# DOCTOR MENU
# ---------------------------------------------------------
def doctor_menu(doctor_id: str):
    while True:
        print("\n========== DOCTOR MENU ==========")
        print("""
        1. View Today's Appointments
        2. Access Patient Records
        3. Add Diagnosis & Prescription
        4. Update Appointment Status
        5. Request Lab Tests

        6. Logout
        """)

        valid = ["1","2","3","4","5","6"]

        while True:
            c = input("Enter choice: ")
            if c in valid:
                break
            print("Invalid choice, enter again.")

        if c == "1": DoctorManagementLib.view_todays_appointments(doctor_id)
        elif c == "2": DoctorManagementLib.access_patient_records(doctor_id)
        elif c == "3": DoctorManagementLib.add_diagnosis_and_prescription(doctor_id)
        elif c == "4": DoctorManagementLib.update_appointment_status(doctor_id)
        elif c == "5": DoctorManagementLib.request_lab_tests(doctor_id)
        elif c == "6": break


# ---------------------------------------------------------
# LAB TECH MENU
# ---------------------------------------------------------
def lab_menu():
    while True:
        print("\n========== LAB TECHNICIAN MENU ==========")
        print("""
        1. View Pending Lab Tests
        2. Enter Lab Result
        3. View Completed Tests

        4. Generate Lab Bill
        5. List Lab Bills

        6. Logout
        """)

        valid = ["1","2","3","4","5","6"]

        while True:
            c = input("Enter choice: ")
            if c in valid:
                break
            print("Invalid choice, enter again.")

        if c == "1": LabManagementLib.view_pending_tests()
        elif c == "2": LabManagementLib.enter_lab_result()
        elif c == "3": LabManagementLib.view_completed_tests()
        elif c == "4": LabManagementLib.generate_lab_bill()
        elif c == "5": LabManagementLib.list_lab_bills()
        elif c == "6": break


# ---------------------------------------------------------
# MAIN
# ---------------------------------------------------------
def main():
    while True:
        print("\n========== WELCOME TO CLINICAL MANAGEMENT SYSTEM ==========")

        staff = login()
        if not staff:
            continue

        role = staff.get_role().lower()

        # ADMIN
        if role == "admin":
            admin_menu()

        # RECEPTION
        elif role == "receptionist":
            reception_menu()

        # DOCTOR
        elif role == "doctor":
            # Find doctor_id from staff_id
            doctors = admin_dao.list_all_doctors()
            doctor_id = None
            for d in doctors:
                if d.get_staff_id() == staff.get_staff_id():
                    doctor_id = d.get_doctor_id()
                    break

            if not doctor_id:
                print("Doctor profile not found. Contact admin.")
                continue

            doctor_menu(doctor_id)

        # LAB TECH
        elif role == "lab technician":
            lab_menu()

        else:
            print("Unknown role. Contact admin.")


if __name__ == "__main__":
    main()