# Generated by Django 4.0.3 on 2022-03-15 09:25

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('pamphlet', '0011_rename_currentunilateralfriendship_unilateralfriendshiprecord'),
    ]

    operations = [
        migrations.RenameField(
            model_name='friendrequestentry',
            old_name='friend',
            new_name='target',
        ),
    ]
