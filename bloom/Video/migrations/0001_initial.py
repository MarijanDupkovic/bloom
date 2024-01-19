# Generated by Django 5.0.1 on 2024-01-18 03:24

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='VideoItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100, unique=True)),
                ('created_at', models.DateField(default=datetime.date.today, verbose_name='Created At')),
                ('video_file', models.FileField(blank=True, null=True, upload_to='videos')),
                ('video_file_1080p', models.FileField(blank=True, null=True, upload_to='videos')),
            ],
        ),
    ]
