from django.db import models
from django_mysql.models import ListTextField

# Create your models here.	

class Team(models.Model):
    """
    Team Model
    - Each team name is unique and has a one-to-one relation to the account that created it
    - Members field will be seperated by '\n' for DOMJudge
    team password (domjudge login) - User.objects.make_random_password(length=10)
    """
    DIVISION = (
        (1, 'Upper Division'),
        (2, 'Lower Division')
    )
    
    name = models.CharField(max_length=30, unique=True)
    division = models.PositiveSmallIntegerField(choices=DIVISION)
    pin = models.CharField(max_length=4, unique=True)
    contest_id = models.CharField(max_length=7, unique=True, blank=True, null=True)
    contest_password = models.CharField(max_length=10, unique=True, blank=True, null=True)
    members = ListTextField(base_field=models.CharField(max_length=181), size=3, max_length=(181 * 3), default=[])
    num_members = models.PositiveSmallIntegerField(default=1)

    def __str__(self):
        return (str(self.name) + ' : ' + str(self.division))
    
