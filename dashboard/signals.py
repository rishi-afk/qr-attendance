from django.db.models.signals import post_save
from django.dispatch import receiver
from django.db.models import Q
import pytz
from dashboard.models import Attendance, Record, TimeTable

DAYS = {0: 'monday', 1: 'tuesday',
        2: 'wednesday', 3: 'thursday', 4: 'friday'}

IST = pytz.timezone('Asia/Kolkata')


@receiver(post_save, sender=Record)
def mark_attendance(_, instance, created, **kwargs):
    if not created:
        date = instance.date
        entry_time = instance.entry_time
        exit_time = instance.exit_time
        c1 = Q(start__range=(entry_time, exit_time))
        c2 = Q(end__range=(entry_time, exit_time))
        periods = getattr(TimeTable.objects.get(
            course=instance.student.course), DAYS[date.weekday()]).filter(c1 & c2).values()
        Attendance.objects.create(record=instance, periods=periods)
