# Generated by Django 3.1 on 2020-09-09 18:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('manager', '0005_auto_20200903_0349'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='role',
            field=models.PositiveSmallIntegerField(choices=[(1, 'Contestant'), (2, 'Proctor'), (3, 'Question Writer')], default=1),
        ),
    ]