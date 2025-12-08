from Dao.LabTechDaoImple import LabTechDaoImplementation
from Dao.ReceptionDaoImple import ReceptionDaoImplementation 
from models.lab_result import LabResult
from models.lab_bill import LabBill

from validation.lab_validation import validate_lab_result_inputs
from validation.common_validation import validate_positive_number


class LabManagementLib:

    dao = LabTechDaoImplementation()
    reception_dao = ReceptionDaoImplementation()

    # --------------------------------------------------------
    # VIEW PENDING LAB TESTS
    # --------------------------------------------------------
    @staticmethod
    def view_pending_tests():
        print("\n--- PENDING LAB TESTS ---")
        tests = LabManagementLib.dao.list_pending_tests()
        if not tests:
            print("No pending tests.")
            return
        for t in tests:
            print(t)

    # --------------------------------------------------------
    # ENTER LAB RESULT
    # --------------------------------------------------------
    @staticmethod
    def enter_lab_result():
        # show pending tests first
        pending = LabManagementLib.dao.list_pending_tests()
        if not pending:
            print("No pending tests.")
            return

        print("\n--- PENDING TESTS ---")
        for t in pending:
            print(t)

        lab_test_id = input("\nEnter Lab Test ID to enter results: ")

        while True:
            try:
                print("\n--- ENTER RESULT DETAILS ---")
                observations = input("Observations: ")
                parameters = input("Parameters (comma separated): ")

                v = validate_lab_result_inputs(observations, parameters)

                result = LabResult(
                    lab_test_id=lab_test_id,
                    observations=v["observations"],
                    parameters=v["parameters"],
                    # result_date auto with datetime.now() in model
                )

                result_id = LabManagementLib.dao.save_lab_result(result)
                if result_id:
                    print(f"Result Saved. RESULT ID: {result_id}")

                    # After saving result, mark test completed
                    LabManagementLib.dao.set_lab_test_completed(lab_test_id)
                    print("Lab Test Status Updated to Completed.\n")
                else:
                    print("Error saving result.")
                break

            except Exception as e:
                print("Validation Error:", e)
                print("Please re-enter.\n")

    # --------------------------------------------------------
    # VIEW COMPLETED TESTS
    # --------------------------------------------------------
    @staticmethod
    def view_completed_tests():
        print("\n--- COMPLETED TESTS ---")
        tests = LabManagementLib.dao.list_completed_tests()
        if not tests:
            print("No completed tests.")
            return
        for t in tests:
            print(t)

    # --------------------------------------------------------
    # GENERATE LAB BILL
    # --------------------------------------------------------
    @staticmethod
    def generate_lab_bill():
        print("\n--- GENERATE LAB BILL ---")
        lab_test_id = input("Enter Lab Test ID: ")

        # NEW VALIDATION
        lab_test = LabManagementLib.dao.get_lab_test_by_id(lab_test_id)
        if not lab_test:
            print("Invalid Lab Test ID. Cannot generate bill.")
            return

        patient_id = lab_test["patient_id"]

        amt = input("Enter Total Amount: ")
        try:
            total = validate_positive_number(amt)
        except Exception as e:
            print("Invalid amount:", e)
            return

        lb = LabBill(
            patient_id=patient_id,
            total_amount=total,
            status="Paid",
        )

        lb_id = LabManagementLib.dao.generate_lab_bill(lb)
        if lb_id:
            # fetch patient name
            patient = LabManagementLib.reception_dao.search_patient_by_id(patient_id)
            pname = patient.get_name() if patient else "Unknown"

            print("\n--- LAB BILL SUMMARY ---")
            print(f"Bill ID     : {lb_id}")
            print(f"Lab Test ID : {lab_test_id}")
            print(f"Patient     : {pname} ({patient_id})")
            print(f"Amount      : {total}")
            print(f"Status      : Paid")
        else:
            print("Failed to generate laboratory bill.")


    # --------------------------------------------------------
    # LIST LAB BILLS
    # --------------------------------------------------------
    @staticmethod
    def list_lab_bills():
        print("\n--- LAB BILLS ---")
        bills = LabManagementLib.dao.list_lab_bills()
        if not bills:
            print("No lab bills found.")
            return

        for b in bills:
            print(b)