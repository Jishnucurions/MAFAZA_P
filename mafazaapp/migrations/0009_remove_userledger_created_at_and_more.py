# Generated by Django 5.1.7 on 2025-03-22 19:56

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('mafazaapp', '0008_remove_transaction_last_calculated'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='userledger',
            name='created_at',
        ),
        migrations.RemoveField(
            model_name='userledger',
            name='receipt',
        ),
    ]
