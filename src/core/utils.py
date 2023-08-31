import string
import secrets


def make_random_password(length):
        alphabet = string.ascii_letters + string.digits

        while True:
            password = ''.join(secrets.choice(alphabet) for i in range(length))
            if (any(c.islower() for c in password)
                and any(c.isupper() for c in password)
                and any(c.isdigit() for c in password)):
                break

        return password
