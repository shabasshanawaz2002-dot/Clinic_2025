from datetime import datetime, date, time

class Bill:
    def _init_(
        self,
        bill_id: str = None,
        appointment_id: str = None,
        patient_id: str = None,
        doctor_id: str = None,
        amount: float = None,
        status: str = "Paid",
        generated_date: datetime = None,
    ):
        self.__bill_id = bill_id
        self.__appointment_id = appointment_id
        self.__patient_id = patient_id
        self.__doctor_id = doctor_id
        self.__amount = amount
        self.__status = status
        self.__generated_date = generated_date or datetime.now()

    # getters/setters
    def get_bill_id(self): return self.__bill_id
    def set_bill_id(self, v): self.__bill_id=v

    def get_appointment_id(self): return self.__appointment_id
    def set_appointment_id(self, v): self.__appointment_id=v

    def get_patient_id(self): return self.__patient_id
    def set_patient_id(self, v): self.__patient_id=v

    def get_doctor_id(self): return self.__doctor_id
    def set_doctor_id(self, v): self.__doctor_id=v

    def get_amount(self): return self.__amount
    def set_amount(self, v): self.__amount=v

    def get_status(self): return self.__status
    def set_status(self, v): self.__status=v

    def get_generated_date(self): return self.__generated_date
    def set_generated_date(self, v): self.__generated_date=v

    def _str_(self):
        return (
            f"{self._bill_id} | A:{self.appointment_id} | P:{self._patient_id} | "
            f"D:{self._doctor_id} | {self.amount} | {self._status}"
        )