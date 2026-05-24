import re


def validate_email(email):

    pattern = r"^[\w\.-]+@[\w\.-]+\.\w+$"

    return re.match(pattern, email)


def validate_password(password):

    if len(password) < 6:
        return False

    return True

def validate_budget(min_budget, max_budget):
    
    try:
        min_budget = int(min_budget)
        max_budget = int(max_budget)

        # Prevent zero or negative values
        if min_budget <= 0 or max_budget <= 0:
            return False

        # Ensure min is not greater than max
        if min_budget > max_budget:
            return False

        return True

    except ValueError:
        return False

def validate_region(region):

    valid_regions = [
        "Mainland",
        "Island"
    ]

    return region in valid_regions


def validate_empty_fields(*fields):

    for field in fields:

        if not field.strip():
            return False

    return True