from django.contrib import admin
from import_export import fields, resources
from import_export.admin import ImportExportModelAdmin
from import_export.widgets import ForeignKeyWidget

from . import models

# Register your models here.

class ProfileAdmin(admin.ModelAdmin):
    # list_display field incompatible with the "user__first|last_name" format
    list_display = ("last_name", "first_name", "role",)
    list_filter = ("role", "checked_in",)
    search_fields = ["user__last_name", "user__first_name"]

    def first_name(self, obj):
        return obj.user.first_name
    
    def last_name(self, obj):
        return obj.user.last_name


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


admin.site.register(models.Profile, ProfileAdmin)
admin.site.register(models.Faculty, FacultyAdmin)
admin.site.register(models.Course, CourseAdmin)
