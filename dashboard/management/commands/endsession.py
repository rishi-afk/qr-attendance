import logging
from django.core.management.base import BaseCommand, CommandError
from dashboard.models import Student, Record
from django.conf import settings
from datetime import datetime


class Command(BaseCommand):
    help = 'Marks attendance for all absent students'

    def handle(self, *args, **options):
        TODAY = datetime.now(settings.IST).date()
        # Procedure 1
        try:
            no_exits = Record.objects.filter(
                date=TODAY, exit_time__isnull=True)
            for record in no_exits:
                record.absent = True
                record.save()
            self.stdout.write(self.style.SUCCESS(
                'Session_End: Procedure #1 Successfull'))
        except:
            logging.exception("Session_End: Procedure #1 Failed")
            raise CommandError(
                'Session_End: Procedure #1 Failed')

        # Procedure 2
        try:
            marked = Record.objects.filter(
                date=TODAY).values_list('student_id', flat=True)
            students = Student.objects.exclude(id__in=marked)
            for student in students:
                record = Record(student=student, date=TODAY,
                                entry_time=settings.DEFAULT_ATTENDANCE_ENTRY_TIME, absent=True)
                record.save()
            self.stdout.write(self.style.SUCCESS(
                'Session_End: Procedure #2 Successfull'))
        except:
            logging.exception("Session_End: Procedure #2 Failed")
            raise CommandError('Session_End: Procedure #2 Failed')
