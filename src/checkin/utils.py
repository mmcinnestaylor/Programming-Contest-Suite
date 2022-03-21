def checkin_auth(user):
	return user.profile.is_volunteer() or user.is_superuser
