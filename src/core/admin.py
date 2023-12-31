from django.contrib import admin
from django.contrib.auth.models import User

from import_export import resources
from import_export.admin import ImportExportModelAdmin


class UserResource(resources.ModelResource):
	"""
	Attach User model to Django-Import-Export
	https://django-import-export.readthedocs.io/en/latest/getting_started.html#creating-a-resource
	"""
	class Meta:
		model = User
		fields = ('first_name', 'last_name', 'email', 'is_active', 'profile__checked_in')


class UserAdmin(ImportExportModelAdmin):
    """
    Django-Import-Export resource admin intrgration
    https://django-import-export.readthedocs.io/en/latest/advanced_usage.html#admin-integration
    """
	
    resource_class = UserResource
    list_display = ("last_name", "first_name", "username", "email", "is_active",)
    list_filter = ("is_active",)
    search_fields = ["last_name", "first_name", "username", "email"]


# Re-register User model for django-import-export integration
admin.site.unregister(User)
admin.site.register(User, UserAdmin)
