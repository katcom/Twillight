# Generated by Django 4.0.3 on 2022-03-22 10:32

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import pamphlet.utils


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('pamphlet', '0024_alter_statusentryimage_status_entry_avatarentry'),
    ]

    operations = [
        migrations.CreateModel(
            name='LikesEntry',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('creation_date', models.DateField(auto_now_add=True)),
                ('status', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='likes', to='pamphlet.statusentry')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='likes', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AlterField(
            model_name='avatarentry',
            name='avatar_image',
            field=models.ImageField(blank=True, default='images/defaults/default-avatar-alien.png', null=True, upload_to=pamphlet.utils.getAvatarFilePathByUsername),
        ),
        migrations.AlterField(
            model_name='avatarentry',
            name='user',
            field=models.OneToOneField(on_delete=django.db.models.deletion.DO_NOTHING, related_name='avatar', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='facepamphletuser',
            name='user',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='face_pamphlet_account', to=settings.AUTH_USER_MODEL),
        ),
        migrations.DeleteModel(
            name='ValidUnilateralFriendship',
        ),
    ]
