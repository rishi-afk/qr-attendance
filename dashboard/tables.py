import django_tables2 as tables
from .models import Attendance


class AttendanceTable(tables.Table):
    class Meta:
        model = Attendance
        template_name = "django_tables2/bootstrap.html"
        fields = (
            "record__date", 'attended', "total")
