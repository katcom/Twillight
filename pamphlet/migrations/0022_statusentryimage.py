# Generated by Django 4.0.3 on 2022-03-18 14:31

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('pamphlet', '0021_privatechatroom_privatechatroom_unique user pair_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='StatusEntryImage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image_file', models.ImageField(blank=True, null=b'I01\n', upload_to='')),
                ('thumbnail', models.ImageField(null=True, upload_to='')),
                ('description', models.CharField(blank=True, default='', max_length=128, null=True)),
                ('status_entry', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='pamphlet.statusentry')),
            ],
        ),
    ]
