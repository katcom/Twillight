# Generated by Django 4.0.3 on 2022-03-24 16:28

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('pamphlet', '0033_alter_userdescription_user'),
    ]

    operations = [
        migrations.DeleteModel(
            name='UserDescription',
        ),
    ]
