# Generated by Django 3.2.15 on 2022-09-04 07:19

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('lfg', '0002_lfgprofile'),
    ]

    operations = [
        migrations.AddField(
            model_name='lfgprofile',
            name='completed',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='lfgprofile',
            name='discord_discriminator',
            field=models.SmallIntegerField(validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(9999)]),
        ),
    ]
