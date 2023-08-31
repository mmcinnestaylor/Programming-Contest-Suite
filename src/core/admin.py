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
    list_display = ("last_name", "first_name", "username", "email", "is_active",)
    list_filter = ("is_active",)
    search_fields = ["last_name", "first_name", "username", "email"]


# Register your models here.
admin.site.unregister(User)
admin.site.register(User, UserAdmin)
