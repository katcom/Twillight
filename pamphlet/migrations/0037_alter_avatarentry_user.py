# Generated by Django 4.0.3 on 2022-03-25 18:32

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('pamphlet', '0036_alter_userdescription_user'),
    ]

    operations = [
        migrations.AlterField(
            model_name='avatarentry',
            name='user',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='avatar', to=settings.AUTH_USER_MODEL),
        ),
    ]
