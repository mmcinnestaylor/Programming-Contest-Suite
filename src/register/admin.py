from django.contrib import admin

from . import models

# Register your models here.

admin.site.register(models.Course)
admin.site.register(models.Faculty)
admin.site.register(models.Profile)
admin.site.register(models.Team)