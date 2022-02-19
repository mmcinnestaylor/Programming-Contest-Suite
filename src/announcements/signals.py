from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import Announcement
from .tasks import email_annoucement


@receiver(post_save, sender=Announcement)
def send_announcement(sender, instance, created, **kwargs):
	# Publish
	if instance.status == 1:
		email_annoucement.delay(instance.id)
	# Draft
	else:
		pass
