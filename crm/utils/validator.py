from email_validator import validate_email, EmailNotValidError


def check_mail(email_adress: str):
    """
    Function to check if the email provided by the user is correct
    Take a String as an Argument
    return True if mail is correct and False if it is not
    """
    try:
        email = validate_email(email_adress, check_deliverability=False)
        return True
    except EmailNotValidError as e:
        return False
