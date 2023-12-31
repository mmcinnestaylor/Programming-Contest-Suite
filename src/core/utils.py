import string
import secrets


def make_random_password(length):
    """
    Basic password generator. Utilizes an alphanumeric alphabet.
    - password must contain at least 1 upper case letter, 1 lower case letter, and 1 number

    length(int): target character length of password
    """

    alphabet = string.ascii_letters + string.digits

    while True:
        password = ''.join(secrets.choice(alphabet) for i in range(length))
        # Check string against requirements (upper + lower + digit)
        if (any(c.islower() for c in password)
            and any(c.isupper() for c in password)
            and any(c.isdigit() for c in password)):
            break

    return password
