from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import Announcement
from .tasks import email_annoucement, discord_announcement


@receiver(post_save, sender=Announcement)
def send_announcement(sender, instance, created, **kwargs):
	# Publish
	if instance.status == 1:
		if instance.send_email:
			email_annoucement.delay(instance.id)
		if instance.send_discord:
			discord_announcement.delay(instance.id)
	# Draft
	else:
		pass
