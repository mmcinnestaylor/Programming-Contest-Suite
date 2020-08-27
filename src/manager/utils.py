def has_team(user):
    return user.profile.has_team()


def has_no_team(user):
    return not user.profile.has_team()


def team_admin(user):
	return user.profile.team_admin


def not_registered(user):
	return not user.is_authenticated
