from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from django.db.models import Q, Count
from dashboard.models import Attendance, Record, TimeTable

DAYS = {0: 'monday', 1: 'tuesday',
        2: 'wednesday', 3: 'thursday', 4: 'friday'}


@receiver(post_save, sender=Record)
def mark_attendance(sender, instance, created, **kwargs):
    if created and instance.absent == True:
        # TODO: schedule a job at 6PM to iterate through all the students and if an attendance record does not exist,
        # create a record with absent = True
        # this signal will recieve it and mark not attended for all lectures for that day
        total_papers = getattr(TimeTable.objects.get(
            course=instance.student.course), DAYS[date.weekday()]).values("paper").annotate(total=Count('paper'))
        attendance_count = [{'paper_id': paper['paper'], 'total':paper['total'],
                             'attended': 0} for paper in total_papers]
        bulk_attendance = []
        for attendance in attendance_count:
            paper_id = attendance.get('paper_id')
            total = attendance.get('total')
            attended = attendance.get('attended')
            bulk_attendance.append(Attendance(
                record=instance, paper_id=paper_id, total=total, attended=attended))
        Attendance.objects.bulk_create(bulk_attendance)

    if not created and instance.entry_time and instance.exit_time:
        date = instance.date
        entry_time = instance.entry_time
        exit_time = instance.exit_time
        c1 = Q(start__range=(entry_time, exit_time))
        c2 = Q(end__range=(entry_time, exit_time))
        periods = getattr(TimeTable.objects.get(
            course=instance.student.course), DAYS[date.weekday()]).filter(c1 & c2)
        periods_attended = periods.values(
            "paper").annotate(attended=Count('paper'))
        attended = {period["paper"]: period["attended"]
                    for period in periods_attended}

        total_papers = getattr(TimeTable.objects.get(
            course=instance.student.course), DAYS[date.weekday()]).values("paper").annotate(total=Count('paper'))

        attendance_count = [{'paper_id': paper['paper'], 'total':paper['total'],
                             'attended': attended.get(paper['paper'], 0)} for paper in total_papers]
        bulk_attendance = []
        for attendance in attendance_count:
            paper_id = attendance.get('paper_id')
            total = attendance.get('total')
            attended = attendance.get('attended')
            bulk_attendance.append(Attendance(
                record=instance, paper_id=paper_id, total=total, attended=attended))
        Attendance.objects.bulk_create(bulk_attendance)
