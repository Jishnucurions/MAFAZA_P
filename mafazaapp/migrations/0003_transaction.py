# Generated by Django 5.1.6 on 2025-03-20 19:42

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mafazaapp', '0002_assignedproject'),
    ]

    operations = [
        migrations.CreateModel(
            name='Transaction',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.DecimalField(decimal_places=2, max_digits=15)),
                ('transaction_type', models.CharField(choices=[('investment', 'Investment'), ('withdrawal', 'Withdrawal')], max_length=20)),
                ('narration', models.TextField(blank=True, null=True)),
                ('receipt', models.FileField(blank=True, null=True, upload_to='transaction_receipts/')),
                ('status', models.CharField(choices=[('pending', 'Pending'), ('approved', 'Approved'), ('rejected', 'Rejected')], default='pending', max_length=20)),
                ('transaction_date', models.DateTimeField(auto_now_add=True)),
                ('return_period', models.CharField(blank=True, max_length=20, null=True)),
                ('return_amount', models.DecimalField(blank=True, decimal_places=2, max_digits=15, null=True)),
                ('project', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='transactions', to='mafazaapp.investmentproject')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='transactions', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
