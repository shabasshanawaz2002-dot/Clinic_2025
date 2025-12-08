import re

def validate_name(name: str):
    if not name:
        raise Exception("Name cannot be empty")
    pattern = r"^[A-Za-z\s]{3,50}$"
    if not re.match(pattern, name):
        raise Exception("Name must contain only letters and spaces (3-50 characters)")
    return name


def validate_phone(phone: str):
    if not phone:
        raise Exception("Phone is required")
    pattern = r"^[6-9]\d{9}$"
    if not re.match(pattern, phone):
        raise Exception("Invalid phone number format")
    return phone


def validate_gender(gender: str):
    if gender not in ["Male", "Female", "Other"]:
        raise Exception("Gender must be Male/Female/Other")
    return gender


def validate_positive_number(value: str):
    try:
        v = float(value)
    except:
        raise Exception("Enter numeric value only")
    if v < 0:
        raise Exception("Value cannot be negative")
    return v