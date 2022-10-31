from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from django.db.models import Q
import pytz
from dashboard.models import Attendance, Record, TimeTable
from django.core.exceptions import ValidationError

DAYS = {0: 'monday', 1: 'tuesday',
        2: 'wednesday', 3: 'thursday', 4: 'friday'}

IST = pytz.timezone('Asia/Kolkata')


@receiver(pre_save, sender=TimeTable)
def validate_time_table(sender, instance: TimeTable, **kwargs):

    monday = list(instance.monday.values_list("start", "end"))
    tuesday = list(instance.tuesday.values_list("start", "end"))
    wednesday = list(instance.wednesday.values_list("start", "end"))
    thursday = list(instance.thursday.values_list("start", "end"))
    friday = list(instance.friday.values_list("start", "end"))

    if (set(monday) == monday and set(tuesday) == tuesday and set(wednesday) == wednesday and set(thursday) == thursday and set(friday) == friday):
        return
    raise ValidationError("Invalid Timetable")


@receiver(post_save, sender=Record)
def mark_attendance(sender, instance, created, **kwargs):
    if not created and instance.entry_time and instance.exit_time:
        date = instance.date
        entry_time = instance.entry_time
        exit_time = instance.exit_time
        c1 = Q(start__range=(entry_time, exit_time))
        c2 = Q(end__range=(entry_time, exit_time))
        periods = getattr(TimeTable.objects.get(
            course=instance.student.course), DAYS[date.weekday()]).filter(c1 & c2).values_list('id', flat=True)
        attendance = Attendance.objects.create(record=instance)
        attendance.periods.set(periods)
