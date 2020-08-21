from django.contrib import admin
from import_export import resources
from import_export.admin import ImportExportModelAdmin

from . import models

# Register your models here.

class FacultyResource(resources.ModelResource):
	class Meta:
		model = models.Faculty
		import_id_fields = ('email',)


class FacultyAdmin(ImportExportModelAdmin):
    resource_class = FacultyResource


class CourseResource(resources.ModelResource):
	class Meta:
		model = models.Course
		#import_id_fields = ('email',)

admin.site.register(models.Course)
admin.site.register(models.Profile)
admin.site.register(models.Faculty, FacultyAdmin)
