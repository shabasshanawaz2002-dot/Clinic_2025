from datetime import datetime, date, time

class LabTestOrder:
    def __init__(
        self,
        lab_test_id: str = None,
        appointment_id: str = None,
        patient_id: str = None,
        doctor_id: str = None,
        token_no: str = None,
        test_name: str = None,
        notes: str = None,
        status: str = "Pending",
    ):
        self.__lab_test_id = lab_test_id
        self.__appointment_id = appointment_id
        self.__patient_id = patient_id
        self.__doctor_id = doctor_id
        self.__token_no = token_no
        self.__test_name = test_name
        self.__notes = notes
        self.__status = status

    # Getters / Setters
    def get_lab_test_id(self): return self.__lab_test_id
    def set_lab_test_id(self, v): self.__lab_test_id=v

    def get_appointment_id(self): return self.__appointment_id
    def set_appointment_id(self, v): self.__appointment_id=v

    def get_patient_id(self): return self.__patient_id
    def set_patient_id(self, v): self.__patient_id=v

    def get_doctor_id(self): return self.__doctor_id
    def set_doctor_id(self, v): self.__doctor_id=v

    def get_token_no(self): return self.__token_no
    def set_token_no(self, v): self.__token_no=v

    def get_test_name(self): return self.__test_name
    def set_test_name(self, v): self.__test_name=v

    def get_notes(self): return self.__notes
    def set_notes(self, v): self.__notes=v

    def get_status(self): return self.__status
    def set_status(self, v): self.__status=v

    def __str__(self):
        return (
            f"{self.__lab_test_id} | P:{self.__patient_id} | D:{self.__doctor_id} | "
            f"{self.__test_name} | T:{self.__token_no} | {self.__status}"
        )
