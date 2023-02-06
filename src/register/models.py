from django.db import models
from django.contrib.auth.models import User


# Create your models here.	

class Team(models.Model):
    """
    Team Model
    - name attribute is unique but not primary key
    - division is the contest division
    - pin used to allow nonmembers to join team
    - contest_id used by domjudge as team login username
    - contest_password used by domjudge as team login password
    - num_members used to avoid extra DB queries
    """
    DIVISION = (
        (1, 'Upper Division'),
        (2, 'Lower Division')
    )
    
    name = models.CharField(max_length=30, unique=True)
    division = models.PositiveSmallIntegerField(choices=DIVISION)
    pin = models.CharField(max_length=6, unique=True)
    contest_id = models.CharField(max_length=7, unique=True, blank=True, null=True)
    contest_password = models.CharField(max_length=6, unique=True, blank=True, null=True)
    questions_answered = models.PositiveSmallIntegerField(default=0)
    num_members = models.PositiveSmallIntegerField(default=0)

    def __str__(self):
        return (str(self.name) + ' : ' + ('U' if self.division == 1 else 'L'))

    def get_members(self):
        members = User.objects.filter(profile__team=self)

        member_names = []
        for member in members:
            member_names.append(member.first_name+' '+member.last_name)

        return member_names

    def is_active(self):
        members = User.objects.filter(profile__team=self)

        for member in members:
            if member.profile.checked_in == True:
                return True
        
        return False
