from django.core.management.base import BaseCommand, CommandError
from dashboard.models import Student, Record
from datetime import datetime
import pytz
IST = pytz.timezone('Asia/Kolkata')


class Command(BaseCommand):
    help = 'Marks attendance for all absent students'

    def handle(self, *args, **options):
        DEFAULT_ENTRY_TIME = datetime.now(IST).replace(
            hour=9, minute=0, second=0, microsecond=0)

        TODAY = datetime.now(IST).date()
        try:
            today = datetime(2022, 11, 18)
            marked = Record.objects.filter(
                date=today).values_list('student_id', flat=True)
            students = Student.objects.exclude(id__in=marked)
            for student in students:
                record = Record(student=student, date=today,
                                entry_time=DEFAULT_ENTRY_TIME, absent=True)
                record.save()
            self.stdout.write(self.style.SUCCESS(
                'Successfully marked absentees'))
        except:
            raise CommandError('Error in marking attendance')
