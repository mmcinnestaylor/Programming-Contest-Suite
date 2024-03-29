"""
Functions useable by @user_passes_test view decorator
"""

def checkin_auth(user):
	"""
	Determines if a user is a contest volnuteer or system superuser.
	"""

	return user.profile.is_volunteer() or user.is_superuser
