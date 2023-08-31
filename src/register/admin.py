from django.contrib import admin

from . import models

# Register your models here.

class TeamAdmin(admin.ModelAdmin):
    list_display = ("name", "num_members", "division", "faculty")
    list_filter = ("division", "faculty")
    search_fields = ["name"]

admin.site.register(models.Team, TeamAdmin)