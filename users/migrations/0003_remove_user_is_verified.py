# Generated by Django 4.2.4 on 2023-09-03 18:19

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_user_country_user_is_verified_user_verification_key_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='is_verified',
        ),
    ]
