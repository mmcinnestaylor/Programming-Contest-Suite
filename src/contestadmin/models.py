from django.db import models
from django.contrib.auth.models import User
from django_mysql.models import ListTextField


# Create your models here.

class Contest(models.Model):
    """
    Contest Model
    - Results field for DOMJudge contest results uploading
    """

    results = models.FileField(upload_to='uploads/')
        
    def __str__(self):
        return ("Programming Contest")
