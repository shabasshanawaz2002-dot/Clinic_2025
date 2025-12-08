from datetime import datetime, date, time

class Doctor:
    def __init__(
        self,
        doctor_id: str = None,
        staff_id: str = None,
        specialization: str = None,
        consultation_fee: float = None,
        working_hours: str = None,
        status: str = "Active",
    ):
        self.__doctor_id = doctor_id
        self.__staff_id = staff_id
        self.__specialization = specialization
        self.__consultation_fee = consultation_fee
        self.__working_hours = working_hours
        self.__status = status

    # Getters
    def get_doctor_id(self): return self.__doctor_id
    def get_staff_id(self): return self.__staff_id
    def get_specialization(self): return self.__specialization
    def get_consultation_fee(self): return self.__consultation_fee
    def get_working_hours(self): return self.__working_hours
    def get_status(self): return self.__status

    # Setters
    def set_doctor_id(self, v): self.__doctor_id=v
    def set_staff_id(self, v): self.__staff_id=v
    def set_specialization(self, v): self.__specialization=v
    def set_consultation_fee(self, v): self.__consultation_fee=v
    def set_working_hours(self, v): self.__working_hours=v
    def set_status(self, v): self.__status=v

    def __str__(self):
        return f"{self.__doctor_id} | Staff:{self.__staff_id} | {self.__specialization}"
