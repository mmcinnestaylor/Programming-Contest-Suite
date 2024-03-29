"""
Functions useable by @user_passes_test view decorator. Each function accepts a User object
as its only parameter.
"""

def has_team(user):
    return user.profile.has_team()


def has_no_team(user):
    return not user.profile.has_team()


def team_admin(user):
	return user.profile.team_admin


def not_registered(user):
	return not user.is_authenticated


def has_fsuid(user):
	return user.profile.fsu_id is not None
