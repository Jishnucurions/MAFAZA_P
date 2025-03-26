# Generated by Django 5.1.7 on 2025-03-26 08:56

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mafazaapp', '0016_remove_passwordresetrequest_is_processed_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserDocument',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('document_type', models.CharField(choices=[('PASSPORT', 'Passport'), ('EMIRATES_ID', 'Emirates ID'), ('CONTRACT', 'Agreement/Contract'), ('PROOF_OF_ADDRESS', 'Proof of Address'), ('BANK_STATEMENT', 'Bank Statement'), ('SELFIE', 'Selfie with ID'), ('OTHER', 'Other')], max_length=20)),
                ('file', models.FileField(upload_to='user_documents/')),
                ('status', models.CharField(choices=[('PENDING', 'Pending Review'), ('APPROVED', 'Approved'), ('REJECTED', 'Rejected - Needs Resubmission')], default='PENDING', max_length=20)),
                ('uploaded_at', models.DateTimeField(auto_now_add=True)),
                ('reviewed_at', models.DateTimeField(blank=True, null=True)),
                ('rejection_reason', models.TextField(blank=True, null=True)),
                ('expiration_date', models.DateField(blank=True, null=True)),
                ('is_primary', models.BooleanField(default=False)),
                ('reviewed_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='reviewed_documents', to=settings.AUTH_USER_MODEL)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='documents', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'User Document',
                'verbose_name_plural': 'User Documents',
                'ordering': ['-uploaded_at'],
            },
        ),
    ]
