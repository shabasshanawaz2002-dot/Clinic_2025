from abc import ABC, abstractmethod
from typing import List, Optional
from models.staff import Staff
from models.doctor import Doctor


class AdminDaoService(ABC):

    # ---- Login ----
    @abstractmethod
    def authenticate_staff(self, username: str, password: str) -> Optional[Staff]:
        """Return staff object if valid, otherwise None"""
        pass

    # ---- Staff ----
    @abstractmethod
    def add_staff(self, staff: Staff) -> str:
        """Insert staff and return generated staff_id (STxxx)"""
        pass

    @abstractmethod
    def search_staff_by_id(self, staff_id: str) -> Optional[Staff]:
        pass

    @abstractmethod
    def search_staff_by_phone(self, phone: str) -> Optional[Staff]:
        pass

    @abstractmethod
    def list_all_staff(self) -> List[Staff]:
        pass

    @abstractmethod
    def update_staff(self, staff: Staff) -> bool:
        pass

    @abstractmethod
    def deactivate_staff(self, staff_id: str) -> bool:
        pass

    # ---- Doctor profile ----
    @abstractmethod
    def add_doctor_profile(self, doctor: Doctor) -> str:
        """Return doctor_id (DRxxx)"""
        pass

    @abstractmethod
    def update_doctor_profile(self, doctor: Doctor) -> bool:
        pass

    @abstractmethod
    def list_all_doctors(self) -> List[Doctor]:
        pass

    @abstractmethod
    def find_doctor_by_id(self, doctor_id: str) -> Optional[Doctor]:
        pass