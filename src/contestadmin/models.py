from django.db import models
from django.contrib.auth.models import User


# Create your models here.

class Contest(models.Model):
    """
    Contest Model
    - Results field for DOMJudge contest results uploading
    """

    contest_date = models.DateField(auto_now=False)
    contest_doors = models.TimeField(auto_now=False)
    contest_start = models.TimeField(auto_now=False)
    contest_freeze = models.TimeField(auto_now=False)
    contest_end = models.TimeField(auto_now=False)
    contest_awards = models.TimeField(auto_now=False)
    results = models.FileField(upload_to='uploads/', blank=True)
    ec_processed = models.BooleanField(default=False)
        
    def __str__(self):
        return ("Programming Contest "+str(self.contest_date))
