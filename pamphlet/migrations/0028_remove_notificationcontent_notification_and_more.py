# Generated by Django 4.0.3 on 2022-03-23 07:25

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('pamphlet', '0027_notification_notificationcontent'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='notificationcontent',
            name='notification',
        ),
        migrations.DeleteModel(
            name='Notification',
        ),
        migrations.DeleteModel(
            name='NotificationContent',
        ),
    ]