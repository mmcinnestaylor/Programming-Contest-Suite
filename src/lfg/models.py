from django.db import models


# Create your models here.

class DiscordMember(models.Model):
    username = models.CharField(max_length=32)
    discriminator = models.SmallIntegerField()

    def __str__(self):
        return (str(self.username)+'#'+str(self.discriminator).zfill(4))
