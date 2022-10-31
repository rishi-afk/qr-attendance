# Generated by Django 4.1.2 on 2022-10-31 17:49

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='period',
            name='paper',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='dashboard.paper'),
        ),
        migrations.AlterField(
            model_name='record',
            name='exit_time',
            field=models.TimeField(blank=True, null=True),
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