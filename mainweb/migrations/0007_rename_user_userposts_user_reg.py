# Generated by Django 3.2 on 2022-03-07 16:59

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('mainweb', '0006_auto_20220307_1653'),
    ]

    operations = [
        migrations.RenameField(
            model_name='userposts',
            old_name='user',
            new_name='user_reg',
        ),
    ]
