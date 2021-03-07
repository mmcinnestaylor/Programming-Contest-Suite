from django.db import models
from django.contrib.auth.models import User
from django_mysql.models import ListTextField


# Create your models here.

class Contest(models.Model):
    """
    Contest Model
    - Results field for DOMJudge contest results uploading
    """

    contest_date = models.DateTimeField(auto_now=False)
    results = models.FileField(upload_to='uploads/', blank=True)
    ec_processed = models.BooleanField(default=False)
        
    def __str__(self):
        return ("Programming Contest")
