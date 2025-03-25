# Generated by Django 5.1.7 on 2025-03-22 20:20

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mafazaapp', '0009_remove_userledger_created_at_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='userledger',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='userledger',
            name='receipt',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]
