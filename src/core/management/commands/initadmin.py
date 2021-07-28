from django.contrib.auth.models import User, UserManager
from django.core.management.base import BaseCommand

class Command(BaseCommand):

    def handle(self, *args, **options):
        if User.objects.count() == 0:
            admin = UserManager.create_superuser(username='dev', email='webmaster@fsu.acm.org', password='seminoles1!')
            admin.save()
        else:
            print('Admin accounts can only be initialized if no Accounts exist')