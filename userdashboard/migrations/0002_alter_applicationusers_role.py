# Generated by Django 3.2 on 2022-01-30 09:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('userdashboard', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='applicationusers',
            name='role',
            field=models.CharField(blank=True, choices=[('USER', 'USER'), ('UNIVERSITY-ADMIN', 'UNIVERSITY-ADMIN')], default='USER', max_length=20, null=True),
        ),
    ]
