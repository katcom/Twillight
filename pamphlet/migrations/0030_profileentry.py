# Generated by Django 4.0.3 on 2022-03-24 16:18

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import pamphlet.utils


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('pamphlet', '0029_notification_notificationcontent'),
    ]

    operations = [
        migrations.CreateModel(
            name='ProfileEntry',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('background_image', models.ImageField(blank=True, null=True, upload_to=pamphlet.utils.getProfileBackgroundFilePathByUsername)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.DO_NOTHING, related_name='profile', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]