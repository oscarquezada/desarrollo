# Generated by Django 5.1.3 on 2024-11-28 01:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0002_event_eventimage_comment'),
    ]

    operations = [
        migrations.AddField(
            model_name='event',
            name='is_deleted',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='eventimage',
            name='is_deleted',
            field=models.BooleanField(default=False),
        ),
    ]
