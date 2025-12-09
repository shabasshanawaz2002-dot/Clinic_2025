from validation.common_validation import validate_name, validate_phone, validate_gender

def validate_patient_inputs(name, age, blood_group, gender, phone, address, emergency):
    errors = []   # collect all errors and raise once

    # ---- ALL FIELDS REQUIRED ----
    required_fields = {
        "Name": name,
        "Age": age,
        "Blood Group": blood_group,
        "Gender": gender,
        "Phone": phone,
        "Address": address,
        "Emergency Contact": emergency
    }

    for field, value in required_fields.items():
        if not value or str(value).strip() == "":
            errors.append(f"{field} is required")

    # validate name
    try:
        name = validate_name(name)
    except Exception as e:
        errors.append(str(e))

    # validate phone
    try:
        phone = validate_phone(phone)
    except Exception as e:
        errors.append(str(e))

    # validate gender
    try:
        gender = validate_gender(gender)
    except Exception as e:
        errors.append(str(e))

    # validate blood group
    valid_blood_groups = ["A+","A-","B+","B-","AB+","AB-","O+","O-"]
    if blood_group and blood_group not in valid_blood_groups:
        errors.append("Invalid blood group. Must be one of: A+, A-, B+, B-, AB+, AB-, O+, O-")

    # validate emergency contact format
    if emergency:
        if not emergency.isdigit() or len(emergency) != 10:
            errors.append("Emergency contact must be 10 digits")

    # validate age
    try:
        age_int = int(age)
        if age_int <= 0 or age_int > 120:
            errors.append("Age must be between 1 and 120")
    except:
        errors.append("Age must be numeric")

    # raise all errors at once
    if errors:
        raise Exception("\n".join(errors))

    return {
        "name": name,
        "age": age_int,
        "blood_group": blood_group,
        "gender": gender,
        "phone": phone,
        "address": address,
        "emergency_contact": emergency,
    }
