from datetime import datetime, date, time

class Patient:
    def __init__(
        self,
        patient_id: str = None,
        name: str = None,
        age: int = None,
        blood_group: str = None,
        gender: str = None,
        phone: str = None,
        address: str = None,
        emergency_contact: str = None,
    ):
        self.__patient_id = patient_id
        self.__name = name
        self.__age = age
        self.__blood_group = blood_group
        self.__gender = gender
        self.__phone = phone
        self.__address = address
        self.__emergency_contact = emergency_contact

    # Getters
    def get_patient_id(self): return self.__patient_id
    def get_name(self): return self.__name
    def get_age(self): return self.__age
    def get_blood_group(self): return self.__blood_group
    def get_gender(self): return self.__gender
    def get_phone(self): return self.__phone
    def get_address(self): return self.__address
    def get_emergency_contact(self): return self.__emergency_contact

    # Setters
    def set_patient_id(self, v): self.__patient_id=v
    def set_name(self, v): self.__name=v
    def set_age(self, v): self.__age=v
    def set_blood_group(self, v): self.__blood_group=v
    def set_gender(self, v): self.__gender=v
    def set_phone(self, v): self.__phone=v
    def set_address(self, v): self.__address=v
    def set_emergency_contact(self, v): self.__emergency_contact=v

    def __str__(self):
        return f"{self.__patient_id} | {self.__name} | {self.__phone}"