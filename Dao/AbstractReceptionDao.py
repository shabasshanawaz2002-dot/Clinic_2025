from abc import ABC, abstractmethod
from typing import List, Optional
from models.patient import Patient
from models.appointment import Appointment
from models.bill import Bill


class ReceptionDaoService(ABC):

    # ---- Patient ----
    @abstractmethod
    def add_patient(self, patient: Patient) -> str:
        pass

    @abstractmethod
    def search_patient_by_id(self, patient_id: str) -> Optional[Patient]:
        pass

    @abstractmethod
    def search_patient_by_phone(self, phone: str) -> Optional[Patient]:
        pass

    @abstractmethod
    def list_all_patients(self) -> List[Patient]:
        pass

    # ---- Appointment ----
    @abstractmethod
    def create_appointment(self, appointment: Appointment) -> str:
        """Return appointment_id (Axxx)"""
        pass

    @abstractmethod
    def list_today_appointments(self) -> List[Appointment]:
        pass

    @abstractmethod
    def cancel_appointment(self, appointment_id: str) -> bool:
        pass

    # ---- Billing (consultation) ----
    @abstractmethod
    def generate_consultation_bill(self, bill: Bill) -> str:
        """Return bill_id (Bxxx)"""
        pass

    @abstractmethod
    def list_consultation_bills(self) -> List[Bill]:
        pass