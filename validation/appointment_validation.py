from datetime import datetime, date, time


# ------------------------------------------------------------
# Validate appointment date + time (base format checking)
# ------------------------------------------------------------
def validate_appointment_inputs(date_input: str, time_input: str):
    """
    Convert string date and string time into datetime.date and datetime.time
    used for scenarios where date input is provided. Here we keep this
    for compatibility, but Reception side now forces today automatically.
    """

    # validate date format
    try:
        appt_date = datetime.strptime(date_input, "%d/%m/%Y").date()
    except:
        raise Exception("Invalid appointment date format. Use DD/MM/YYYY")

    # validate time format
    try:
        appt_time = datetime.strptime(time_input, "%H:%M").time()
    except:
        raise Exception("Invalid time format. Use HH:MM (24-hour format)")

    return {
        "appointment_date": appt_date,
        "appointment_time": appt_time
    }



# ------------------------------------------------------------
# Validate doctor working hours + enforce today and future time
# ------------------------------------------------------------
def validate_doctor_time(working_hours: str, input_time: str):
    """
    Checks if given appointment time lies within doctor's working hours
    and ensures appointment date is today and time is future.
    
    working_hours example: "10AM-4PM"
    input_time example: "10:30"
    """

    # working hour format must contain '-'
    try:
        parts = working_hours.split("-")
        if len(parts) != 2:
            raise Exception("Doctor working hours are not properly configured")

        start_str = parts[0].strip()   # e.g. "10AM"
        end_str   = parts[1].strip()   # e.g. "4PM"

        # convert "10AM" -> time(10,00) using datetime.strptime("%I%p")
        start_time = datetime.strptime(start_str, "%I%p").time()
        end_time   = datetime.strptime(end_str, "%I%p").time()

    except Exception:
        raise Exception("Invalid working hours format in doctor profile")

    # convert user input HH:MM -> time
    try:
        given_time = datetime.strptime(input_time, "%H:%M").time()
    except:
        raise Exception("Invalid time format. Use HH:MM in 24-hour format")

    # enforce appointment is for today only (Reception-> today)
    today = date.today()

    # ensure within working-hours range
    if not (start_time <= given_time <= end_time):
        raise Exception(
            f"Appointment must be between "
            f"{start_time.strftime('%I:%M %p')} and "
            f"{end_time.strftime('%I:%M %p')}"
        )

    # ensure future time (NOT earlier than now)
    now = datetime.now().time()
    if today == date.today() and given_time <= now:
        raise Exception("Appointment time must be in the future today")

    return given_time