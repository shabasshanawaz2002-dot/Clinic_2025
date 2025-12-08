from validation.common_validation import validate_name, validate_phone, validate_gender, validate_positive_number
from validation.date_time_validation import validate_date

def validate_staff_inputs(name, phone, address, age, gender, email, role, username, password, qualifications, joining_date, salary):
    name = validate_name(name)
    phone = validate_phone(phone)
    gender = validate_gender(gender)
    salary = validate_positive_number(salary)
    joining_date = validate_date(joining_date)

    if not address:
        raise Exception("Address required")
    if not role:
        raise Exception("Role required")
    if not username:
        raise Exception("Username required")
    if not password:
        raise Exception("Password required")
    if not email:
        raise Exception("Email required")

    return {
        "name": name,
        "phone": phone,
        "address": address,
        "age": int(age),
        "gender": gender,
        "email": email,
        "role": role,
        "username": username,
        "password": password,
        "qualifications": qualifications,
        "date_of_joining": joining_date,
        "salary": float(salary)
    }