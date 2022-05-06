from django.contrib import admin
from django.contrib.auth.models import User

from import_export import resources
from import_export.admin import ImportExportModelAdmin


class UserResource(resources.ModelResource):
	class Meta:
		model = User
		fields = ('first_name', 'last_name', 'email', 'is_active', 'profile__checked_in')


class UserAdmin(ImportExportModelAdmin):
    resource_class = UserResource


# Register your models here.
admin.site.unregister(User)
admin.site.register(User, UserAdmin)
