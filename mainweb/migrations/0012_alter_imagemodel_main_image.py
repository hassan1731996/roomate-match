# Generated by Django 3.2 on 2022-03-08 10:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mainweb', '0011_alter_imagemodel_main_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='imagemodel',
            name='main_image',
            field=models.ImageField(null=True, upload_to='images/'),
        ),
    ]
