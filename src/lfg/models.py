from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator, MinValueValidator 

# Create your models here.

class DiscordMember(models.Model):
    """
    Discord user model which stores the username and discriminator
    of a full Discord username.

    *** IMPORTANT Dec 2023 *** Discord has updated their username format and
    no longer utilizes discriminators. This model MUST be updated to support
    the new format.
    """

    username = models.CharField(max_length=32)
    discriminator = models.SmallIntegerField()

    def __str__(self):
        return (str(self.username)+'#'+str(self.discriminator).zfill(4))


class LFGProfile(models.Model):
    """
    Looking For Group Profile model. Each instance is tied to a single contestant.

    *** IMPORTANT Dec 2023 *** Discord has updated their username format and
    no longer utilizes discriminators. This model MUST be updated to support
    the new format.

    discord_username
    discord_discriminator
    ***

    user: the user instance attached to an LFG profile

    division: division in which a contestant wants to compete

    standing: participant's collegiate standing

    active: If False, the profile is inactive and not participating in the LFG service. If
        True the profile is active and particpating in LFG.

    completed: If False, the profile is incomplete, if True the profile is complete.

    verified: If False, the profile is unverified, meaning the username has not
        yet been matched to a member of the target Discord server. If True, the
        username has been matched.
    """

    DIVISION = (
        (1, 'Upper Division'),
        (2, 'Lower Division')
    )

    STANDING = (
        (1, 'Graduate'),
        (2, 'Senior'),
        (3, 'Junior'),
        (4, 'Sophomore'),
        (5, 'Freshman'),
        (6, 'Other'),
    )

    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    discord_username = models.CharField(max_length=32)
    discord_discriminator = models.SmallIntegerField(validators=[MinValueValidator(0), MaxValueValidator(9999)])
    division = models.PositiveSmallIntegerField(
        choices=DIVISION, blank=True, null=True)
    standing = models.PositiveSmallIntegerField(
        choices=STANDING, blank=True, null=True)
    active = models.BooleanField(default=False)
    completed = models.BooleanField(default=False)
    verified = models.BooleanField(default=False)

    def __str__(self):
        return (str(self.user.first_name) + ' ' + str(self.user.last_name)+' - '+str(self.discord_username)+'#'+str(self.discord_discriminator).zfill(4))

    def get_discord_username(self):
        return str(self.discord_username)+'#'+str(self.discord_discriminator).zfill(4)

    def is_completed(self):
        return self.division is not None and self.standing is not None

    def is_activatable(self):
        return not self.active and self.completed and self.verified 
