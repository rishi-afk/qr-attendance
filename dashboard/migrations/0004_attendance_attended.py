# Generated by Django 4.1.2 on 2022-11-06 10:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0003_remove_attendance_period'),
    ]

    operations = [
        migrations.AddField(
            model_name='attendance',
            name='attended',
            field=models.SmallIntegerField(default=0),
            preserve_default=False,
        ),
    ]
