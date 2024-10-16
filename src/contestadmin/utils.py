from django.contrib.auth.mixins import UserPassesTestMixin

"""
Functions useable by @user_passes_test view decorator. Each function accepts a User object
as its only parameter.
"""

def contestadmin_auth(user):
    return user.profile.role == 5 or user.is_superuser


class ContestAdminAuthMixin(UserPassesTestMixin):
    """
    Mixin which integrates the contestadmin_auth test into a UserPassesTestMixin.
    - Enables class based view support of the test.
    """

    def test_func(self):
        return contestadmin_auth(self.request.user)
