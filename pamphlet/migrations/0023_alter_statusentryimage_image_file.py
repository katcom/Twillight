# Generated by Django 4.0.3 on 2022-03-18 15:49

from django.db import migrations, models
import pamphlet.utils


class Migration(migrations.Migration):

    dependencies = [
        ('pamphlet', '0022_statusentryimage'),
    ]

    operations = [
        migrations.AlterField(
            model_name='statusentryimage',
            name='image_file',
            field=models.ImageField(blank=True, null=b'I01\n', upload_to=pamphlet.utils.getStatusFilePathByUsername),
        ),
    ]
