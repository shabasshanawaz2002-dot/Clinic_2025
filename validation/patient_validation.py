from validation.common_validation import validate_name, validate_phone, validate_gender

def validate_patient_inputs(name, age, blood_group, gender, phone, address, emergency):
    name = validate_name(name)
    phone = validate_phone(phone)
    gender = validate_gender(gender)

    if not blood_group:
        raise Exception("Blood group required")
    if not address:
        raise Exception("Address required")
    if not emergency:
        raise Exception("Emergency contact required")

    return {
        "name": name,
        "age": int(age),
        "blood_group": blood_group,
        "gender": gender,
        "phone": phone,
        "address": address,
        "emergency_contact": emergency,
    }