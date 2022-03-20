def contestadmin_auth(user):
	return user.profile.role == 4 or user.is_superuser
