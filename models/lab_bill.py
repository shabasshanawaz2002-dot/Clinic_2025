from datetime import datetime, date, time

class LabBill:
    def __init__(
        self,
        lab_bill_id: str = None,
        patient_id: str = None,
        total_amount: float = None,
        status: str = "Pending",
        generated_date: datetime = None,
    ):
        self.__lab_bill_id = lab_bill_id
        self.__patient_id = patient_id
        self.__total_amount = total_amount
        self.__status = status
        self.__generated_date = generated_date or datetime.now()

    # getters/setters
    def get_lab_bill_id(self): return self.__lab_bill_id
    def set_lab_bill_id(self, v): self.__lab_bill_id=v

    def get_patient_id(self): return self.__patient_id
    def set_patient_id(self, v): self.__patient_id=v

    def get_total_amount(self): return self.__total_amount
    def set_total_amount(self, v): self.__total_amount=v

    def get_status(self): return self.__status
    def set_status(self, v): self.__status=v

    def get_generated_date(self): return self.__generated_date
    def set_generated_date(self, v): self.__generated_date=v

    def __str__(self):
        return (
            f"{self.__lab_bill_id} | P:{self.__patient_id} | "
            f"Total:{self.__total_amount} | {self.__status}"
        )