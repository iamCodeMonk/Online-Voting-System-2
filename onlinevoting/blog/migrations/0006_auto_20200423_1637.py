# Generated by Django 3.0.4 on 2020-04-23 16:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0005_society_whoallvoted'),
    ]

    operations = [
        migrations.AddField(
            model_name='society',
            name='Participation_on',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='society',
            name='Voting_on',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='society',
            name='Voting_process_on',
            field=models.BooleanField(default=False),
        ),
    ]
