# Generated by Django 3.0.3 on 2020-04-21 15:11

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0002_society_post'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='society',
            name='post',
        ),
    ]
