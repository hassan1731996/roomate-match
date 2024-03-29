# Generated by Django 3.2 on 2022-03-09 11:39

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mainweb', '0012_alter_imagemodel_main_image'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='userposts',
            name='title',
        ),
        migrations.AlterField(
            model_name='userposts',
            name='date',
            field=models.DateField(default=datetime.date(2022, 3, 9)),
        ),
        migrations.AlterField(
            model_name='userposts',
            name='no_of_bathrooms',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='userposts',
            name='no_of_bedrooms',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]
