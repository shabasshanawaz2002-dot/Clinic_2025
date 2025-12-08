from datetime import datetime, date, time

class Staff:
    def __init__(
        self,
        staff_id: str = None,
        name: str = None,
        phone: str = None,
        address: str = None,
        age: int = None,
        gender: str = None,
        email: str = None,
        role: str = None,
        username: str = None,
        password: str = None,
        qualifications: str = None,
        date_of_joining: date = None,
        salary: float = None,
        status: str = "Active",
    ):
        self.__staff_id = staff_id
        self.__name = name
        self.__phone = phone
        self.__address = address
        self.__age = age
        self.__gender = gender
        self.__email = email
        self.__role = role
        self.__username = username
        self.__password = password
        self.__qualifications = qualifications
        self.__date_of_joining = date_of_joining or date.today()
        self.__salary = salary
        self.__status = status

    # Getters
    def get_staff_id(self): return self.__staff_id
    def get_name(self): return self.__name
    def get_phone(self): return self.__phone
    def get_address(self): return self.__address
    def get_age(self): return self.__age
    def get_gender(self): return self.__gender
    def get_email(self): return self.__email
    def get_role(self): return self.__role
    def get_username(self): return self.__username
    def get_password(self): return self.__password
    def get_qualifications(self): return self.__qualifications
    def get_date_of_joining(self): return self.__date_of_joining
    def get_salary(self): return self.__salary
    def get_status(self): return self.__status

    # Setters
    def set_staff_id(self, v): self.__staff_id=v
    def set_name(self, v): self.__name=v
    def set_phone(self, v): self.__phone=v
    def set_address(self, v): self.__address=v
    def set_age(self, v): self.__age=v
    def set_gender(self, v): self.__gender=v
    def set_email(self, v): self.__email=v
    def set_role(self, v): self.__role=v
    def set_username(self, v): self.__username=v
    def set_password(self, v): self.__password=v
    def set_qualifications(self, v): self.__qualifications=v
    def set_date_of_joining(self, v): self.__date_of_joining=v
    def set_salary(self, v): self.__salary=v
    def set_status(self, v): self.__status=v

    def __str__(self):
        return f"{self.__staff_id} | {self.__name} | {self.__role} | {self.__status}"