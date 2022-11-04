from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from django.db.models import Q
from dashboard.models import Attendance, Record, TimeTable

DAYS = {0: 'monday', 1: 'tuesday',
        2: 'wednesday', 3: 'thursday', 4: 'friday'}


@receiver(post_save, sender=Record)
def mark_attendance(sender, instance, created, **kwargs):
    if not created and instance.entry_time and instance.exit_time:
        date = instance.date
        entry_time = instance.entry_time
        exit_time = instance.exit_time
        c1 = Q(start__range=(entry_time, exit_time))
        c2 = Q(end__range=(entry_time, exit_time))
        periods = getattr(TimeTable.objects.get(
            course=instance.student.course), DAYS[date.weekday()]).filter(c1 & c2)
        print(periods)
        bulk_attendance = []
        for period in periods:
            bulk_attendance.append(Attendance(
                record=instance, period=period, paper=period.paper))
        Attendance.objects.bulk_create(bulk_attendance)
