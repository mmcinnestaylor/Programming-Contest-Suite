# Generated by Django 3.2.12 on 2022-03-21 21:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('contestadmin', '0002_auto_20220320_2211'),
    ]

    operations = [
        migrations.AddField(
            model_name='contest',
            name='participation',
            field=models.PositiveSmallIntegerField(blank=True, choices=[(1, 'In-Person'), (2, 'Virtual'), (3, 'Hybrid')], null=True),
        ),
    ]
