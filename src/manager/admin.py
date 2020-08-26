from django.contrib import admin
from import_export import fields, resources
from import_export.admin import ImportExportModelAdmin
from import_export.widgets import ForeignKeyWidget

from . import models

# Register your models here.

class FacultyResource(resources.ModelResource):
	class Meta:
		model = models.Faculty
		import_id_fields = ('email',)


class FacultyAdmin(ImportExportModelAdmin):
    resource_class = FacultyResource


class CourseResource(resources.ModelResource):
	instructor = fields.Field(column_name='instructor',attribute='instructor',widget=ForeignKeyWidget(models.Faculty))
	class Meta:
		model = models.Course


class CourseAdmin(ImportExportModelAdmin):
    resource_class = CourseResource


admin.site.register(models.Profile)
admin.site.register(models.Faculty, FacultyAdmin)
admin.site.register(models.Course, CourseAdmin)
