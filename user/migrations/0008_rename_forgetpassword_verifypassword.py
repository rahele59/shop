# Generated by Django 5.1.4 on 2025-01-01 18:14

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0007_rename_time_forgetpassword_time_created'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='ForgetPassword',
            new_name='VerifyPassword',
        ),
    ]