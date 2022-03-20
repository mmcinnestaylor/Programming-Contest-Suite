from django.db import models
from django.contrib.auth.models import User

from register.models import Team

# Create your models here.

class Faculty(models.Model):
    """
    Faculty Model
    - Email address used as primary key due to guaranteed uniqueness
    - Imported by contest organizers before registration opens 
    """

    email = models.EmailField(max_length=50, primary_key=True)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
        
    def __str__(self):
        return (str(self.first_name) + ' ' + str(self.last_name))


class Course(models.Model):
    """
    Course Model
    - Courses added manually at the this point in time
    - code = 'COP3014'
    - name = 'Programming I'
    - sections = [1, 2, 3, 4, 5]
    """

    code = models.CharField(max_length=8)
    name = models.CharField(max_length=50)
    instructor = models.ForeignKey(Faculty, on_delete=models.SET_NULL, null=True)

    class Meta:
        ordering = ['code']

    def __str__(self):
        return (str(self.code) + ' : ' + str(self.name) + ' - ' + str(self.instructor.last_name) + ', ' + str(self.instructor.first_name)[0])

    def num_registered(self):
        return Profile.objects.filter(courses=self).count()


class Profile(models.Model):
    """
    Profile Model
    - Extends built-in User model
    - team attaches user to a contest team, if null user listed as 'unnamed team' in contest 
    - team_admin gives user ability to delete team, permission transferrable to other teammate
    - fsu_id used for tracking extra credit participation
    - fsu_num used for swipe checkin
    - courses used for extra credit tracking
    - checked_in used to ensure only active participants get extra credit
    """

    ROLES = (
        (1, 'Contestant'),
        (2, 'Proctor'),
        (3, 'Question Writer'),
        (4, 'Organizer')
    )

    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    role = models.PositiveSmallIntegerField(choices=ROLES, default=1)
    team = models.ForeignKey(Team, related_name='profile_team', on_delete=models.SET_NULL, blank=True, null=True)
    team_admin = models.BooleanField(default=False)
    fsu_id = models.CharField(max_length=8, unique=True, blank=True, null=True)
    fsu_num = models.CharField(max_length=8, unique=True, blank=True, null=True)
    courses = models.ManyToManyField(Course, blank=True)
    checked_in = models.BooleanField(default=False)
    email_confirmed = models.BooleanField(default=False)
    
    def __str__(self):
        return (str(self.user.first_name) + ' ' + str(self.user.last_name))

    def has_team(self):
        return self.team is not None

    def has_courses(self):
        return self.courses.count() != 0

    def is_volunteer(self):
        return self.role > 1
