from Dao.ReceptionDaoImple import ReceptionDaoImplementation
from models.patient import Patient
from models.bill import Bill
from models.appointment import Appointment

from validation.patient_validation import validate_patient_inputs
from validation.appointment_validation import validate_doctor_time

from datetime import datetime


class ReceptionManagementLib:

    dao = ReceptionDaoImplementation()

    # -----------------------------------------------
    # PATIENT MANAGEMENT
    # -----------------------------------------------
    @staticmethod
    def add_patient():
        while True:
            try:
                print("\n--- ADD PATIENT ---")
                name = input("Enter name: ")
                age = input("Enter age: ")
                blood_group = input("Enter blood group: ")
                gender = input("Enter gender: ")
                phone = input("Enter phone: ")
                address = input("Enter address: ")
                emergency = input("Enter emergency contact: ")

                data = validate_patient_inputs(
                    name, age, blood_group, gender, phone, address, emergency
                )

                patient = Patient(
                    name=data["name"],
                    age=data["age"],
                    blood_group=data["blood_group"],
                    gender=data["gender"],
                    phone=data["phone"],
                    address=data["address"],
                    emergency_contact=data["emergency_contact"]
                )

                pid = ReceptionManagementLib.dao.add_patient(patient)
                if pid:
                    print("\nPatient added successfully:", pid)
                else:
                    print("\nSomething went wrong while adding patient.")
                break

            except Exception as e:
                print("Error:", e)
                print("Please re-enter details.\n")


    @staticmethod
    def search_patient():
        pid = input("Enter patient ID: ")
        p = ReceptionManagementLib.dao.search_patient_by_id(pid)
        if p:
            print(p)
        else:
            print("Patient not found")


    @staticmethod
    def search_patient_by_phone():
        phone = input("Enter phone number: ")
        p = ReceptionManagementLib.dao.search_patient_by_phone(phone)
        if p:
            print(p)
        else:
            print("Patient not found")


    @staticmethod
    def list_patients():
        pts = ReceptionManagementLib.dao.list_all_patients()
        if not pts:
            print("No patients found.")
            return
        for p in pts:
            print(p)


    # -----------------------------------------------
    # APPOINTMENT management
    # -----------------------------------------------
    @staticmethod
    def create_appointment():
        while True:
            try:
                print("\n--- CREATE APPOINTMENT ---")
                patient_id = input("Enter patient ID: ")
                doctor_id = input("Enter doctor ID: ")

                # today ONLY
                today = datetime.today().date()

                # get doctor details to check working hours
                doctor = ReceptionManagementLib.dao.get_doctor_by_id(doctor_id)
                if not doctor:
                    print("Doctor not found.")
                    return

                working_hours = doctor["working_hours"]    # example "10AM-4PM"

                # time input
                time_input = input("Enter appointment time (HH:MM): ")

                # validate doctor time
                # returns datetime.time object
                valid_time = validate_doctor_time(working_hours, time_input)

                # construct appointment object
                appointment = Appointment(
                    patient_id=patient_id,
                    doctor_id=doctor_id,
                    appointment_date=today,
                    appointment_time=valid_time,
                    status="Confirmed"
                )

                appt_id = ReceptionManagementLib.dao.create_appointment(appointment)
                if appt_id:
                    print("\nAppointment created successfully.")
                    print("Appointment ID:", appt_id)
                    print("Token No for this appointment:", appointment.get_token_no())
                else:
                    print("Something went wrong while creating appointment.")

                break

            except Exception as e:
                print("Error:", e)
                print("Please re-enter.\n")


    @staticmethod
    def list_todays_appointments():
        appts = ReceptionManagementLib.dao.list_today_appointments()
        if not appts:
            print("No appointments today.")
            return
        for a in appts:
            print(a)


    @staticmethod
    def cancel_appointment():
        appt_id = input("Enter appointment ID: ")
        if ReceptionManagementLib.dao.cancel_appointment(appt_id):
            print("Appointment cancelled.")
        else:
            print("Operation failed.")


    # -----------------------------------------------
    # BILLING
    # -----------------------------------------------
    @staticmethod
    def generate_consultation_bill():
        print("\n--- CONSULTATION BILL ---")
        appt_id = input("Enter appointment ID: ")

        # NEW: fetch appointment
        appt = ReceptionManagementLib.dao.get_appointment_by_id(appt_id)
        if not appt:
            print("Invalid appointment ID")
            return

        patient_id = appt["patient_id"]
        doctor_id = appt["doctor_id"]

        # amount must come from doctor table
        doc = ReceptionManagementLib.dao.get_doctor_by_id(doctor_id)
        if not doc:
            print("Doctor not found")
            return

        amount = float(doc["consultation_fee"])
        now = datetime.now()

        bill = Bill(
            appointment_id=appt_id,
            patient_id=patient_id,
            doctor_id=doctor_id,
            amount=amount,
            generated_date=now,
            status="Paid"
        )

        bid = ReceptionManagementLib.dao.generate_consultation_bill(bill)
        if bid:
            print("\n--- BILL DETAILS ---")

            patient = ReceptionManagementLib.dao.search_patient_by_id(patient_id)
            patient_name = patient.get_name() if patient else "Unknown"

            print(f"Bill ID        : {bid}")
            print(f"Appointment ID : {appt_id}")
            print(f"Patient        : {patient_name} ({patient_id})")
            print(f"Amount         : {amount}")
            print(f"Date           : {now.strftime('%Y-%m-%d %H:%M:%S')}")
            print(f"Status         : Paid")
        else:
            print("Failed to generate bill")


    @staticmethod
    def list_consultation_bills():
        bills = ReceptionManagementLib.dao.list_consultation_bills()
        if not bills:
            print("No bills found.")
            return
        for b in bills:
            print(b)