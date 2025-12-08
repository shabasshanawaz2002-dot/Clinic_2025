def validate_prescription_inputs(symptoms, diagnosis, medication, dosage, duration, notes):
    if not symptoms:
        raise Exception("Symptoms required")
    if not diagnosis:
        raise Exception("Diagnosis required")
    if not medication:
        raise Exception("Medication required")

    # dosage & duration can be strings but must not be empty
    if not dosage:
        raise Exception("Dosage required")
    if not duration:
        raise Exception("Duration required")

    return {
        "symptoms": symptoms,
        "diagnosis": diagnosis,
        "medication": medication,
        "dosage": dosage,
        "duration": duration,
        "notes": notes
    }
