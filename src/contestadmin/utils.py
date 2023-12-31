"""
Functions useable by @user_passes_test view decorator. Each function accepts a User object
as its only parameter.
"""

def contestadmin_auth(user):
	return user.profile.role == 5 or user.is_superuser
