# Generated by Django 3.0.8 on 2020-08-08 01:35

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django_mysql.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0011_update_proxy_permissions'),
    ]

    operations = [
        migrations.CreateModel(
            name='Course',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(max_length=8)),
                ('sections', django_mysql.models.ListTextField(models.IntegerField(), size=10)),
            ],
        ),
        migrations.CreateModel(
            name='Faculty',
            fields=[
                ('email', models.EmailField(max_length=50, primary_key=True, serialize=False)),
                ('first_name', models.CharField(max_length=50)),
                ('last_name', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='Team',
            fields=[
                ('id', models.CharField(max_length=7, primary_key=True, serialize=False)),
                ('name', models.CharField(blank=True, max_length=30, unique=True)),
                ('division', models.PositiveSmallIntegerField(choices=[(1, 'Lower Division'), (2, 'Upper Division')], max_length=1)),
                ('password', models.CharField(max_length=10, unique=True)),
                ('num_members', models.PositiveSmallIntegerField(default=1)),
            ],
        ),
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to=settings.AUTH_USER_MODEL)),
                ('team_admin', models.BooleanField(default=False)),
                ('fsu_id', models.CharField(blank=True, max_length=8, unique=True)),
                ('fsu_num', models.CharField(blank=True, max_length=8, unique=True)),
                ('checked_in', models.BooleanField(default=False)),
                ('courses', models.ManyToManyField(to='register.Course')),
                ('team', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='register.Team')),
            ],
        ),
        migrations.AddField(
            model_name='course',
            name='instructor',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='register.Faculty'),
        ),
    ]