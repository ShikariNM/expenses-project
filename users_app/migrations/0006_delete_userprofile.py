# Generated by Django 5.0.6 on 2024-05-13 08:07

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users_app', '0005_alter_userprofile_user'),
    ]

    operations = [
        migrations.DeleteModel(
            name='UserProfile',
        ),
    ]
