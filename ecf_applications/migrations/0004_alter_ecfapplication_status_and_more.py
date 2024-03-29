# Generated by Django 5.0.2 on 2024-03-15 11:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ecf_applications', '0003_ecfapplicationassessmentcomment_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ecfapplication',
            name='status',
            field=models.PositiveSmallIntegerField(choices=[(1, 'Pending'), (2, 'Action Required'), (3, 'Under Review'), (4, 'Under Exam Board Review'), (5, 'Rejected'), (6, 'Approved')], default=1, verbose_name='status'),
        ),
        migrations.AlterField(
            model_name='ecfapplicationassessment',
            name='status',
            field=models.PositiveSmallIntegerField(choices=[(1, 'Pending'), (2, 'Action Required'), (3, 'Under Review'), (4, 'Under Exam Board Review'), (5, 'Rejected'), (6, 'Approved')], default=1, verbose_name='status'),
        ),
    ]
