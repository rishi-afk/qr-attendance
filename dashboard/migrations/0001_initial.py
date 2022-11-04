# Generated by Django 4.1.2 on 2022-11-03 16:08

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import smart_selects.db_fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Course',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('year', models.PositiveSmallIntegerField()),
                ('title', models.CharField(max_length=30)),
            ],
        ),
        migrations.CreateModel(
            name='Paper',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(max_length=20)),
                ('course', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='dashboard.course')),
            ],
        ),
        migrations.CreateModel(
            name='Period',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('start', models.TimeField()),
                ('end', models.TimeField()),
                ('course', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='dashboard.course')),
                ('paper', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='dashboard.paper')),
            ],
        ),
        migrations.CreateModel(
            name='TimeTable',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('course', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='dashboard.course')),
                ('friday', smart_selects.db_fields.ChainedManyToManyField(blank=True, chained_field='course', chained_model_field='course', related_name='friday', to='dashboard.period')),
                ('monday', smart_selects.db_fields.ChainedManyToManyField(chained_field='course', chained_model_field='course', related_name='monday', to='dashboard.period')),
                ('thursday', smart_selects.db_fields.ChainedManyToManyField(blank=True, chained_field='course', chained_model_field='course', related_name='thursday', to='dashboard.period')),
                ('tuesday', smart_selects.db_fields.ChainedManyToManyField(chained_field='course', chained_model_field='course', related_name='tuesday', to='dashboard.period')),
                ('wednesday', smart_selects.db_fields.ChainedManyToManyField(chained_field='course', chained_model_field='course', related_name='wednesday', to='dashboard.period')),
            ],
        ),
        migrations.CreateModel(
            name='Student',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('roll_number', models.CharField(max_length=20, unique=True)),
                ('course', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='dashboard.course')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Record',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField()),
                ('entry_time', models.TimeField()),
                ('exit_time', models.TimeField(blank=True, null=True)),
                ('student', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='dashboard.student')),
            ],
        ),
        migrations.CreateModel(
            name='Professor',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('employee_id', models.CharField(max_length=50)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='paper',
            name='professor',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='dashboard.professor'),
        ),
        migrations.CreateModel(
            name='Attendance',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('paper', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='dashboard.paper')),
                ('period', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='dashboard.period')),
                ('record', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='dashboard.record')),
            ],
        ),
        migrations.AddConstraint(
            model_name='record',
            constraint=models.CheckConstraint(check=models.Q(('exit_time__isnull', True), ('exit_time__gt', models.F('entry_time')), _connector='OR'), name='check_exit_time'),
        ),
        migrations.AddConstraint(
            model_name='record',
            constraint=models.UniqueConstraint(fields=('student', 'date'), name='student_entry_unique'),
        ),
        migrations.AddConstraint(
            model_name='period',
            constraint=models.CheckConstraint(check=models.Q(('end__gt', models.F('start'))), name='check_end_time'),
        ),
        migrations.AddConstraint(
            model_name='period',
            constraint=models.UniqueConstraint(fields=('paper', 'start', 'end'), name='unique_period_slot'),
        ),
    ]
