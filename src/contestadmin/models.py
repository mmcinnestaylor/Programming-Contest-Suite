from django.db import models
from django.contrib.auth.models import User


# Create your models here.

class Contest(models.Model):
    """
    Contest Model
    - Results field for DOMJudge contest results uploading
    """
    FORMAT = (
        (1, 'In-Person'),
        (2, 'Virtual'),
        (3, 'Hybrid')
    )

    contest_date = models.DateField(auto_now=False)
    contest_doors = models.TimeField(auto_now=False, blank=True, null=True)
    contest_start = models.TimeField(auto_now=False, blank=True, null=True)
    contest_freeze = models.TimeField(auto_now=False, blank=True, null=True)
    contest_end = models.TimeField(auto_now=False, blank=True, null=True)
    contest_awards = models.TimeField(auto_now=False, blank=True, null=True)
    team_deadline = models.DateTimeField(auto_now=False, blank=True, null=True)
    results = models.FileField(upload_to='uploads/', blank=True)
    ec_processed = models.BooleanField(default=False)
    volunteer_pin = models.CharField(max_length=8, default='thankyou')
    participation = models.PositiveSmallIntegerField(choices=FORMAT, blank=True, null=True)
    lunch_form_url = models.URLField(blank=True, null=True)
        
    def __str__(self):
        return ("Programming Contest on "+str(self.contest_date))
