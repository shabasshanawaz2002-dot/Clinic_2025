from validation.common_validation import validate_name, validate_phone, validate_gender, validate_positive_number
from validation.date_time_validation import validate_date
import re

def validate_staff_inputs(name, phone, address, age, gender, email, role, username, password, qualifications, joining_date, salary):

    errors = []

    # ALL fields compulsory
    required_fields = {
        "Name": name,
        "Phone": phone,
        "Address": address,
        "Age": age,
        "Gender": gender,
        "Email": email,
        "Role": role,
        "Username": username,
        "Password": password,
        "Qualifications": qualifications,
        "Joining Date": joining_date,
        "Salary": salary
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

    # validate role
    allowed_roles = ["Admin", "Receptionist", "Doctor", "Lab Technician"]
    if role not in allowed_roles:
        errors.append("Role must be one of: Admin, Receptionist, Doctor, Lab Technician")

    # validate email format (regex)
    email_pattern = r"^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$"
    if email and not re.match(email_pattern, email):
        errors.append("Invalid email format")

    # validate salary
    try:
        salary = validate_positive_number(salary)
    except Exception as e:
        errors.append(str(e))

    # validate joining date
    try:
        joining_date = validate_date(joining_date)
    except Exception as e:
        errors.append(str(e))

    # validate age
    try:
        age_int = int(age)
        if age_int <= 0 or age_int > 120:
            errors.append("Age must be between 1 and 120")
    except:
        errors.append("Age must be numeric")

    # RETURN ALL collected errors
    if errors:
        raise Exception("\n".join(errors))

    # final formatted return
    return {
        "name": name,
        "phone": phone,
        "address": address.strip(),
        "age": age_int,
        "gender": gender,
        "email": email,
        "role": role,
        "username": username,
        "password": password,
        "qualifications": qualifications,
        "date_of_joining": joining_date,
        "salary": float(salary)
    }
