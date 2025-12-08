# from Dao.AdminDaoImple import AdminDaoImplementation
from models.staff import Staff
from models.doctor import Doctor

from validation.staff_validation import validate_staff_inputs
# from validation.common_validation import validate_positive_number


class AdminManagementLib:

    dao = AdminDaoImplementation()

    # --------------------------------------------------------
    # ADD STAFF
    # --------------------------------------------------------
    @staticmethod
    def add_staff():
        while True:
            try:
                print("\n--- ADD STAFF ---")
                name = input("Enter staff name: ")
                phone = input("Enter phone: ")
                address = input("Enter address: ")
                age = input("Enter age: ")
                gender = input("Enter gender (Male/Female/Other): ")
                email = input("Enter email: ")
                role = input("Enter role (Admin/Receptionist/Doctor/Lab Technician): ")
                username = input("Enter username: ")
                password = input("Enter password: ")
                qual = input("Enter qualifications: ")
                doj = input("Enter joining date (DD/MM/YYYY): ")
                salary = input("Enter salary: ")

                data = validate_staff_inputs(
                    name, phone, address, age, gender, email,
                    role, username, password, qual, doj, salary
                )

                staff = Staff(
                    name=data["name"],
                    phone=data["phone"],
                    address=data["address"],
                    age=data["age"],
                    gender=data["gender"],
                    email=data["email"],
                    role=data["role"],
                    username=data["username"],
                    password=data["password"],
                    qualifications=data["qualifications"],
                    date_of_joining=data["date_of_joining"],
                    salary=data["salary"],
                )

                sid = AdminManagementLib.dao.add_staff(staff)
                if sid:
                    print("\nStaff added successfully:", sid)
                else:
                    print("\nSomething went wrong while adding staff.")
                break

            except Exception as e:
                print("Error:", e)
                print("Please re-enter details.\n")

    # --------------------------------------------------------
    # SEARCH STAFF
    # --------------------------------------------------------
    @staticmethod
    def search_staff():
        print("\n--- SEARCH STAFF ---")
        staff_id = input("Enter staff ID: ")
        staff = AdminManagementLib.dao.search_staff_by_id(staff_id)
        if staff:
            print(staff)
        else:
            print("Staff not found")

    @staticmethod
    def search_staff_by_phone():
        print("\n--- SEARCH STAFF ---")
        phone = input("Enter staff phone: ")
        staff = AdminManagementLib.dao.search_staff_by_phone(phone)
        if staff:
            print(staff)
        else:
            print("Staff not found")

    # --------------------------------------------------------
    # LIST ALL STAFF
    # --------------------------------------------------------
    @staticmethod
    def list_staff():
        print("\n--- STAFF LIST ---")
        staff_list = AdminManagementLib.dao.list_all_staff()
        if not staff_list:
            print("No staff records found.")
            return
        for s in staff_list:
            print(s)

    # --------------------------------------------------------
    # UPDATE STAFF
    # --------------------------------------------------------
    @staticmethod
    def update_staff():
        print("\n--- UPDATE STAFF ---")
        staff_id = input("Enter staff ID to update: ")
        staff = AdminManagementLib.dao.search_staff_by_id(staff_id)
        if not staff:
            print("Staff not found")
            return

        print("Leave field blank to keep existing value.")
        new_name = input(f"New name [{staff.get_name()}]: ") or staff.get_name()
        new_phone = input(f"New phone [{staff.get_phone()}]: ") or staff.get_phone()
        new_address = input(f"New address [{staff.get_address()}]: ") or staff.get_address()
        new_salary = input(f"New salary [{staff.get_salary()}]: ") or str(staff.get_salary())
        new_status = input(f"New status (Active/Inactive) [{staff.get_status()}]: ") or staff.get_status()

        try:
            new_salary_val = validate_positive_number(new_salary)
        except Exception as e:
            print("Invalid salary:", e)
            return

        staff.set_name(new_name)
        staff.set_phone(new_phone)
        staff.set_address(new_address)
        staff.set_salary(float(new_salary_val))
        staff.set_status(new_status)

        if AdminManagementLib.dao.update_staff(staff):
            print("Staff updated successfully.")
        else:
            print("Update failed.")

    # --------------------------------------------------------
    # DEACTIVATE STAFF
    # --------------------------------------------------------
    @staticmethod
    def deactivate_staff():
        print("\n--- DEACTIVATE STAFF ---")
        staff_id = input("Enter staff ID: ")
        if AdminManagementLib.dao.deactivate_staff(staff_id):
            print("Staff deactivated.")
        else:
            print("Operation failed. Check staff ID.")

    # --------------------------------------------------------
    # ADD DOCTOR PROFILE (with role check)
    # --------------------------------------------------------
    @staticmethod
    def add_doctor():
        print("\n--- ADD DOCTOR PROFILE ---")
        staff_id = input("Enter staff ID to link as Doctor: ")

        # 1) Check that staff exists
        staff = AdminManagementLib.dao.search_staff_by_id(staff_id)
        if not staff:
            print("Invalid staff ID. Staff record not found.")
            return

        # 2) Check staff role is 'Doctor'
        if staff.get_role().lower() != "doctor":
            print(
                f"Cannot create doctor profile: Staff {staff_id} role is '{staff.get_role()}'. "
                "Role must be 'Doctor'."
            )
            return

        # 3) Check if doctor profile already exists for this staff_id
        doctors = AdminManagementLib.dao.list_all_doctors()
        for d in doctors:
            if d.get_staff_id() == staff_id:
                print("Doctor profile already exists for this staff ID.")
                return

        specialization = input("Enter specialization: ")
        fee = input("Enter consultation fee: ")
        working_hours = input("Enter working hours (e.g., 10AM-4PM): ")

        try:
            fee_val = float(fee)
        except:
            print("Invalid fee. Must be a number.")
            return

        doctor = Doctor(
            staff_id=staff_id,
            specialization=specialization,
            consultation_fee=fee_val,
            working_hours=working_hours,
            status="Active",
        )

        did = AdminManagementLib.dao.add_doctor_profile(doctor)
        if did:
            print("Doctor profile created:", did)
        else:
            print("Something went wrong while adding doctor profile.")

    # --------------------------------------------------------
    # UPDATE DOCTOR PROFILE
    # --------------------------------------------------------
    @staticmethod
    def update_doctor():
        print("\n--- UPDATE DOCTOR PROFILE ---")
        doctor_id = input("Enter doctor ID: ")
        doctor = AdminManagementLib.dao.find_doctor_by_id(doctor_id)
        if not doctor:
            print("Doctor not found")
            return

        print("Leave field blank to keep existing value.")
        new_spec = input(f"New specialization [{doctor.get_specialization()}]: ") or doctor.get_specialization()
        new_fee = input(f"New consultation fee [{doctor.get_consultation_fee()}]: ") or str(doctor.get_consultation_fee())
        new_hours = input(f"New working hours [{doctor.get_working_hours()}]: ") or doctor.get_working_hours()
        new_status = input(f"New status (Active/Inactive) [{doctor.get_status()}]: ") or doctor.get_status()

        try:
            new_fee_val = float(new_fee)
        except:
            print("Invalid fee.")
            return

        doctor.set_specialization(new_spec)
        doctor.set_consultation_fee(new_fee_val)
        doctor.set_working_hours(new_hours)
        doctor.set_status(new_status)

        if AdminManagementLib.dao.update_doctor_profile(doctor):
            print("Doctor profile updated.")
        else:
            print("Update failed.")

    # --------------------------------------------------------
    # LIST DOCTORS
    # --------------------------------------------------------
    @staticmethod
    def list_doctors():
        print("\n--- DOCTOR LIST ---")
        docs = AdminManagementLib.dao.list_all_doctors()
        if not docs:
            print("No doctor profiles found.")
            return
        for d in docs:
            print(d)

    @staticmethod
    def search_doctor_by_id():
        print("\n--- SEARCH DOCTOR ---")
        doctor_id = input("Enter doctor ID: ")
        doctor = AdminManagementLib.dao.find_doctor_by_id(doctor_id)
        if doctor:
            print(doctor)
        else:
            print("Doctor not found")