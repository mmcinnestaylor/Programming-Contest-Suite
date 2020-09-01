from django.db import models
from django_mysql.models import ListTextField

# Create your models here.	

class Team(models.Model):
    """
    Team Model
    - name attribute is unique but not primary key
    - division is the contest division
    - pin used to allow nonmembers to join team
    - contest_id used by domjudge as team login username
    - contest_password used by domjudge as team login password
    - members simple string list to avoid extra DB queries
    - num_members used to avoid extra DB queries
    """
    DIVISION = (
        (1, 'Upper Division'),
        (2, 'Lower Division')
    )
    
    name = models.CharField(max_length=30, unique=True)
    division = models.PositiveSmallIntegerField(choices=DIVISION)
    pin = models.CharField(max_length=4, unique=True)
    contest_id = models.CharField(max_length=7, unique=True, blank=True, null=True)
    contest_password = models.CharField(max_length=6, unique=True, blank=True, null=True)
    members = ListTextField(base_field=models.CharField(max_length=181), size=3, max_length=(181 * 3), default=[])
    num_members = models.PositiveSmallIntegerField(default=1)

    def __str__(self):
        return (str(self.name) + ' : ' + str(self.division))
    
