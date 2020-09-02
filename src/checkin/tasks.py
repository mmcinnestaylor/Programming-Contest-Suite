from django.contrib.auth.models import User
from django.core.mail import send_mail

from celery import shared_task


@shared_task
def send_credentials(username):
    user = User.objects.get(username=username)
    user_email = str(user.email)
    team_id = user.profile.team.contest_id
    team_password = user.profile.team.contest_password

    message = 'Hello ' + str(user.first_name) + ',\nWelcome to this semester\'s ACM Programming Contest! Your DOMJudge credentials are below. Use these credentials when your team logs in to http://domjudge.cs.fsu.edu\nusername: ' + str(team_id) + '\npassword: ' + str(team_password)

    send_mail('Your DOMJudge Credentials', message, 'ACM Programming Contest <contest@fsu.acm.org>', [user_email], fail_silently=False)
