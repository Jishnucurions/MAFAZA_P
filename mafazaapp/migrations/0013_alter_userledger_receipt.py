# Generated by Django 5.1.7 on 2025-03-24 16:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mafazaapp', '0012_alter_userledger_receipt'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userledger',
            name='receipt',
            field=models.FileField(blank=True, null=True, upload_to='transaction_receipts/'),
        ),
    ]
