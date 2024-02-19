# Generated by Django 5.0.2 on 2024-02-15 15:26

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='ECFApplication',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('submission_date', models.DateTimeField(auto_now_add=True)),
                ('status', models.CharField(choices=[('PE', 'Pending'), ('AR', 'Action Required'), ('AP', 'Approved'), ('RE', 'Rejected')], default='PE', max_length=2)),
                ('circumstance', models.CharField(choices=[('SM', 'Short Term Medical'), ('LM', 'Long Term Medical'), ('BE', 'Bereavement'), ('PE', 'Personal'), ('OT', 'Other')], max_length=2)),
                ('start_date', models.DateField()),
                ('end_date', models.DateField(blank=True, null=True)),
                ('description', models.TextField()),
                ('evidence', models.FileField(blank=True, null=True, upload_to='evidence/')),
                ('last_updated', models.DateTimeField(auto_now=True)),
                ('student', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='ECFApplicationModuleAssessment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('module_code', models.CharField(max_length=10)),
                ('assessment', models.CharField(max_length=100)),
                ('action', models.CharField(choices=[('EX', 'Extension'), ('NA', 'Not Assessed'), ('LR', 'Late Penalty Removal'), ('BC', 'Exam Board Consideration'), ('AA', 'Authorised Absence'), ('OT', 'Other')], max_length=2)),
                ('extension_date', models.DateField(blank=True, null=True)),
                ('more_info', models.TextField(blank=True, null=True)),
                ('application', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ecfapps.ecfapplication')),
            ],
        ),
    ]
