from abc import ABC, abstractmethod
from typing import List
from models.appointment import Appointment
from models.prescription import Prescription
from models.lab_test_order import LabTestOrder


class DoctorDaoService(ABC):

    @abstractmethod
    def list_today_appointments(self, doctor_id: str) -> List[Appointment]:
        pass

    @abstractmethod
    def save_prescription(self, prescription: Prescription) -> str:
        """Return prescription_id (PRxxx)"""
        pass

    @abstractmethod
    def update_appointment_status(self, appointment_id: str, status: str) -> bool:
        pass

    @abstractmethod
    def request_lab_test(self, order: LabTestOrder) -> str:
        """Return lab_test_id (LTxxx)"""
        pass

    @abstractmethod
    def view_patient_history(self, patient_id: str) -> List[Prescription]:
        """Return all prescriptions for a patient sorted by date"""
        pass
