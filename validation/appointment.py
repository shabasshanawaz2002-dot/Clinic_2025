from datetime import datetime, date, time

class Appointment:
    def _init_(
        self,
        appointment_id: str = None,
        patient_id: str = None,
        doctor_id: str = None,
        appointment_date: date = None,
        appointment_time: time = None,
        token_no: str = None,
        status: str = "Confirmed",
    ):
        self.__appointment_id = appointment_id
        self.__patient_id = patient_id
        self.__doctor_id = doctor_id
        self.__appointment_date = appointment_date or date.today()
        self.__appointment_time = appointment_time or datetime.now().time()
        self.__token_no = token_no
        self.__status = status

    # Getters
    def get_appointment_id(self): return self.__appointment_id
    def get_patient_id(self): return self.__patient_id
    def get_doctor_id(self): return self.__doctor_id
    def get_appointment_date(self): return self.__appointment_date
    def get_appointment_time(self): return self.__appointment_time
    def get_token_no(self): return self.__token_no
    def get_status(self): return self.__status

    # Setters
    def set_appointment_id(self, v): self.__appointment_id=v
    def set_patient_id(self, v): self.__patient_id=v
    def set_doctor_id(self, v): self.__doctor_id=v
    def set_appointment_date(self, v): self.__appointment_date=v
    def set_appointment_time(self, v): self.__appointment_time=v
    def set_token_no(self, v): self.__token_no=v
    def set_status(self, v): self.__status=v

    def _str_(self):
        return (
            f"{self._appointment_id} | P:{self.patient_id} | D:{self._doctor_id} | "
            f"{self._appointment_date} {self._appointment_time} | "
            f"T:{self._token_no} | {self._status}"
        )