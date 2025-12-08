from abc import ABC, abstractmethod
from typing import List
from models.lab_test_order import LabTestOrder
from models.lab_result import LabResult
from models.lab_bill import LabBill


class LabTechDaoService(ABC):

    @abstractmethod
    def list_pending_tests(self) -> List[LabTestOrder]:
        pass

    @abstractmethod
    def list_completed_tests(self) -> List[LabTestOrder]:
        pass

    @abstractmethod
    def save_lab_result(self, result: LabResult) -> str:
        """Return lab_result_id (LRxxx)"""
        pass

    @abstractmethod
    def set_lab_test_completed(self, lab_test_id: str) -> bool:
        pass

    @abstractmethod
    def generate_lab_bill(self, lab_bill: LabBill) -> str:
        """Return lab_bill_id (LBxxx)"""
        pass

    @abstractmethod
    def list_lab_bills(self) -> List[LabBill]:
        pass