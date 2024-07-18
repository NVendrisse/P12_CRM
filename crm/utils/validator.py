from email_validator import validate_email, EmailNotValidError


def check_mail(email_adress: str):
    try:
        email = validate_email(email_adress, check_deliverability=False)
        return True
    except EmailNotValidError as e:
        return False
