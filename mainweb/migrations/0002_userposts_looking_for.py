# Generated by Django 3.2 on 2022-01-31 11:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mainweb', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='userposts',
            name='looking_for',
            field=models.CharField(blank=True, choices=[('ROOMMATES', 'ROOMMATES'), ('PLACE', 'PLACE')], max_length=20, null=True),
        ),
    ]