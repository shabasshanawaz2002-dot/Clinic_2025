def validate_lab_test_inputs(test_name, notes):
    if not test_name:
        raise Exception("Test name required")
    return {
        "test_name": test_name,
        "notes": notes
    }


def validate_lab_result_inputs(observations, parameters):
    if not observations:
        raise Exception("Observations required")
    if not parameters:
        raise Exception("Parameters required")
    return {
        "observations": observations,
        "parameters": parameters
    }
