from datetime import datetime, date, time

class LabResult:
    def __init__(
        self,
        lab_result_id: str = None,
        lab_test_id: str = None,
        observations: str = None,
        parameters: str = None,
        result_date: datetime = None,
    ):
        self.__lab_result_id = lab_result_id
        self.__lab_test_id = lab_test_id
        self.__observations = observations
        self.__parameters = parameters
        self.__result_date = result_date or datetime.now()

    # Getters / Setters
    def get_lab_result_id(self): return self.__lab_result_id
    def set_lab_result_id(self, v): self.__lab_result_id=v

    def get_lab_test_id(self): return self.__lab_test_id
    def set_lab_test_id(self, v): self.__lab_test_id=v

    def get_observations(self): return self.__observations
    def set_observations(self, v): self.__observations=v

    def get_parameters(self): return self.__parameters
    def set_parameters(self, v): self.__parameters=v

    def get_result_date(self): return self.__result_date
    def set_result_date(self, v): self.__result_date=v

    def __str__(self):
        return f"{self.__lab_result_id} | Test:{self.__lab_test_id} | {self.__result_date}"