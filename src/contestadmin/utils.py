def contestadmin_auth(user):
	return user.profile.role == 5 or user.is_superuser
