from datetime import datetime, date, time

class Prescription:
    def __init__(
        self,
        prescription_id: str = None,
        appointment_id: str = None,
        patient_id: str = None,
        doctor_id: str = None,
        token_no: str = None,
        symptoms: str = None,
        diagnosis: str = None,
        medication: str = None,
        dosage: str = None,
        duration: str = None,
        notes: str = None,
        created_at: datetime = None,
    ):
        self.__prescription_id = prescription_id
        self.__appointment_id = appointment_id
        self.__patient_id = patient_id
        self.__doctor_id = doctor_id
        self.__token_no = token_no
        self.__symptoms = symptoms
        self.__diagnosis = diagnosis
        self.__medication = medication
        self.__dosage = dosage
        self.__duration = duration
        self.__notes = notes
        self.__created_at = created_at or datetime.now()

    # Getters
    def get_prescription_id(self): return self.__prescription_id
    def get_appointment_id(self): return self.__appointment_id
    def get_patient_id(self): return self.__patient_id
    def get_doctor_id(self): return self.__doctor_id
    def get_token_no(self): return self.__token_no
    def get_symptoms(self): return self.__symptoms
    def get_diagnosis(self): return self.__diagnosis
    def get_medication(self): return self.__medication
    def get_dosage(self): return self.__dosage
    def get_duration(self): return self.__duration
    def get_notes(self): return self.__notes
    def get_created_at(self): return self.__created_at

    # Setters
    def set_prescription_id(self, v): self.__prescription_id=v
    def set_appointment_id(self, v): self.__appointment_id=v
    def set_patient_id(self, v): self.__patient_id=v
    def set_doctor_id(self, v): self.__doctor_id=v
    def set_token_no(self, v): self.__token_no=v
    def set_symptoms(self, v): self.__symptoms=v
    def set_diagnosis(self, v): self.__diagnosis=v
    def set_medication(self, v): self.__medication=v
    def set_dosage(self, v): self.__dosage=v
    def set_duration(self, v): self.__duration=v
    def set_notes(self, v): self.__notes=v
    def set_created_at(self, v): self.__created_at=v

    def __str__(self):
        return (
            f"{self.__prescription_id} | A:{self.__appointment_id} | "
            f"P:{self.__patient_id} | D:{self.__doctor_id} | T:{self.__token_no}"
        )
