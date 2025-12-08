from Dao.DoctorDaoImple import DoctorDaoImplementation
from Dao.ReceptionDaoImple import ReceptionDaoImplementation

from models.prescription import Prescription
from models.lab_test_order import LabTestOrder

from validation.prescription_validation import validate_prescription_inputs
from validation.lab_validation import validate_lab_test_inputs


class DoctorManagementLib:

    doctor_dao = DoctorDaoImplementation()
    reception_dao = ReceptionDaoImplementation()

    # 1. VIEW TODAY'S APPOINTMENTS (for this doctor)
    @staticmethod
    def view_todays_appointments(doctor_id: str):
        print("\n--- TODAY'S APPOINTMENTS ---")
        appts = DoctorManagementLib.doctor_dao.list_today_appointments(doctor_id)
        if not appts:
            print("No appointments for today.")
            return

        for a in appts:
            print(
                f"TOKEN: {a.get_token_no()} | "
                f"APT: {a.get_appointment_id()} | "
                f"PATIENT: {a.patient_name} ({a.get_patient_id()}) | "
                f"TIME: {a.get_appointment_time()} | "
                f"STATUS: {a.get_status()}"
            )

    @staticmethod
    def access_patient_records(doctor_id: str):
        """
        Flow:
        1. Doctor enters Patient ID (or chooses from today's list in UI before calling this)
        2. Show:
           - Personal details
           - Today's appointment(s) for this doctor
           - Previous prescriptions
        """
        patient_id = input("Enter Patient ID: ")
        patient = DoctorManagementLib.reception_dao.search_patient_by_id(patient_id)
        if not patient:
            print("No patient found with that ID.")
            return

        print("\n--- PATIENT DETAILS ---")
        print(patient)

        print("\n--- TODAY'S APPOINTMENTS WITH YOU ---")
        todays = DoctorManagementLib.doctor_dao.list_today_appointments(doctor_id)
        found_apt = False
        for a in todays:
            if a.get_patient_id() == patient_id:
                found_apt = True
                print(a)
        if not found_apt:
            print("No appointment today for this patient with you.")

        print("\n--- PREVIOUS PRESCRIPTIONS / HISTORY ---")
        history = DoctorManagementLib.doctor_dao.view_patient_history(patient_id)
        if not history:
            print("No previous prescriptions found.")
        else:
            for p in history:
                print(
                    f"""
        Prescription ID: {p.get_prescription_id()}
        Symptoms: {p.get_symptoms()}
        Diagnosis: {p.get_diagnosis()}
        Medication: {p.get_medication()}
        Dosage: {p.get_dosage()}
        Duration: {p.get_duration()}
        Notes: {p.get_notes()}
        """
                )


    @staticmethod
    def add_diagnosis_and_prescription(doctor_id: str):
        """
        Flow (from document):
        1. Doctor selects appointment from today's list.
        2. System shows:
           - Patient details
           - Previous history/prescriptions
           - Token
        3. Doctor enters:
           - Symptoms, Diagnosis, Medication, Dosage, Duration, Notes
        4. Save prescription linked to:
           - appointment_id, patient_id, doctor_id, token_no
        5. Update appointment status -> Completed
        """
        # Show today's appointments first
        appts = DoctorManagementLib.doctor_dao.list_today_appointments(doctor_id)
        if not appts:
            print("No appointments for today.")
            return

        print("\n--- TODAY'S APPOINTMENTS ---")
        for a in appts:
            print(
                f"TOKEN: {a.get_token_no()} | "
                f"APT: {a.get_appointment_id()} | "
                f"PATIENT: {a.get_patient_id()} | "
                f"TIME: {a.get_appointment_time()} | "
                f"STATUS: {a.get_status()}"
            )

        selected_appt_id = input("\nEnter Appointment ID for consultation: ")
        selected_appt = None
        for a in appts:
            if a.get_appointment_id() == selected_appt_id:
                selected_appt = a
                break

        if not selected_appt:
            print("Appointment ID not found in today's list.")
            return

        # Fetch patient details
        patient = DoctorManagementLib.reception_dao.search_patient_by_id(
            selected_appt.get_patient_id()
        )

        print("\n--- PATIENT DETAILS ---")
        if patient:
            print(patient)
        else:
            print("Patient record not found (data inconsistency).")

        print("\n--- PREVIOUS PRESCRIPTIONS ---")
        history = DoctorManagementLib.doctor_dao.view_patient_history(
            selected_appt.get_patient_id()
        )
        if not history:
            print("No previous prescriptions.")
        else:
            for p in history:
                print(p)

        # Now enter new prescription data with validation loop
        while True:
            try:
                print("\n--- ENTER PRESCRIPTION DETAILS ---")
                symptoms = input("Symptoms: ")
                diagnosis = input("Diagnosis: ")
                medication = input("Medication Name: ")
                dosage = input("Dosage: ")
                duration = input("Duration: ")
                notes = input("Additional Notes: ")

                data = validate_prescription_inputs(
                    symptoms, diagnosis, medication, dosage, duration, notes
                )

                pres = Prescription(
                    appointment_id=selected_appt.get_appointment_id(),
                    patient_id=selected_appt.get_patient_id(),
                    doctor_id=doctor_id,
                    token_no=selected_appt.get_token_no(),
                    symptoms=data["symptoms"],
                    diagnosis=data["diagnosis"],
                    medication=data["medication"],
                    dosage=data["dosage"],
                    duration=data["duration"],
                    notes=data["notes"],
                )

                pid = DoctorManagementLib.doctor_dao.save_prescription(pres)
                if pid:
                    print(f"\nPrescription Saved Successfully. ID: {pid}")
                    DoctorManagementLib.doctor_dao.update_appointment_status(
                        selected_appt.get_appointment_id(), "Completed"
                    )
                    print("Appointment Status Updated to Completed.")
                else:
                    print("Failed to save prescription.")
                break
            except Exception as e:
                print("Validation Error:", e)
                print("Please re-enter prescription details.\n")

    # 4. UPDATE APPOINTMENT STATUS
    @staticmethod
    def update_appointment_status(doctor_id: str):
        """
        Doctor can manually mark appointment as:
        - Completed
        - Revisit Needed
        """
        appts = DoctorManagementLib.doctor_dao.list_today_appointments(doctor_id)
        if not appts:
            print("No appointments for today.")
            return

        print("\n--- TODAY'S APPOINTMENTS ---")
        for a in appts:
            print(
                f"TOKEN: {a.get_token_no()} | "
                f"APT: {a.get_appointment_id()} | "
                f"PATIENT: {a.get_patient_id()} | "
                f"TIME: {a.get_appointment_time()} | "
                f"STATUS: {a.get_status()}"
            )

        appt_id = input("\nEnter Appointment ID to update: ")
        status = input("Enter new status (Completed / Pending): ")

        if DoctorManagementLib.doctor_dao.update_appointment_status(appt_id, status):
            print("Appointment status updated.")
        else:
            print("Failed to update appointment status (check Appointment ID).")

    # 5. REQUEST LAB TESTS
    @staticmethod
    def request_lab_tests(doctor_id: str):
        """
        Flow from document:
        1. Doctor selects appointment (appointment + token)
        2. System shows categories (but here we just accept test name)
        3. Save lab test order with:
           - Order ID (DB auto)
           - Patient ID
           - Appointment ID
           - Doctor ID
           - Token ID
           - Test details / notes
           - Status = Pending
        """
        appts = DoctorManagementLib.doctor_dao.list_today_appointments(doctor_id)
        if not appts:
            print("No appointments for today.")
            return

        print("\n--- TODAY'S APPOINTMENTS ---")
        for a in appts:
            print(
                f"TOKEN: {a.get_token_no()} | "
                f"APT: {a.get_appointment_id()} | "
                f"PATIENT: {a.get_patient_id()} | "
                f"TIME: {a.get_appointment_time()} | "
                f"STATUS: {a.get_status()}"
            )

        selected_appt_id = input("\nEnter Appointment ID to request lab test for: ")
        selected_appt = None
        for a in appts:
            if a.get_appointment_id() == selected_appt_id:
                selected_appt = a
                break

        if not selected_appt:
            print("Appointment ID not found.")
            return

        while True:
            try:
                print("\n--- LAB TEST REQUEST ---")
                test_name = input("Enter Test Name (e.g., Blood CBC, X-Ray, etc.): ")
                notes = input("Enter any notes / instructions: ")

                val = validate_lab_test_inputs(test_name, notes)

                order = LabTestOrder(
                    appointment_id=selected_appt.get_appointment_id(),
                    patient_id=selected_appt.get_patient_id(),
                    doctor_id=doctor_id,
                    token_no=selected_appt.get_token_no(),
                    test_name=val["test_name"],
                    notes=val["notes"],
                    status="Pending",
                )
                order_id = DoctorManagementLib.doctor_dao.request_lab_test(order)
                if order_id:
                    print(f"Lab Test Order Created. ORDER ID: {order_id}")
                    print("\n--- LAB TEST SUMMARY ---")
                    print(f"Test Name  : {val['test_name']}")
                    print(f"Notes      : {val['notes']}")
                    print(f"Status     : Pending")
                    break
                else:
                    print("Failed to create lab test order.")
            except Exception as e:
                print("Error:", e)
                print("Please re-enter lab test details.\n")
