from django.contrib.auth.models import User
from django.core.management.base import BaseCommand

class Command(BaseCommand):
    """
    System startup command to create initial Superuser is no accounts exist.
    """

    def handle(self, *args, **options):
        if User.objects.count() == 0:
            admin = User.objects.create_superuser(username='contestadmin', email='contest@fsu.acm.org', password='seminoles1!', first_name='Administrator')
            admin.save()
            print('INIT: Default admin account created')
        else:
            print('INIT: Admin accounts can only be initialized if no Accounts exist')
