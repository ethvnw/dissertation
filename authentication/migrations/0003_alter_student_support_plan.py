# Generated by Django 5.0.2 on 2024-03-10 14:56

import authentication.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0002_alter_user_managers_alter_student_study_level'),
    ]

    operations = [
        migrations.AlterField(
            model_name='student',
            name='support_plan',
            field=models.FileField(blank=True, null=True, upload_to=authentication.models.Student.gen_file_name),
        ),
    ]
