import django_tables2 as tables
from .models import Attendance


class AttendanceTable(tables.Table):
    class Meta:
        model = Attendance
        template_name = "django_tables2/bootstrap.html"
        fields = (
            "record__date", 'attended', "total")


class AttendanceHistoryTable(tables.Table):
    class Meta:
        model = Attendance
        template_name = "django_tables2/bootstrap.html"
        fields = ("record__student__roll_number",
                  "record__date", 'attended', 'total')


class AttendanceTableProfessor(tables.Table):
    class Meta:
        model = Attendance
        template_name = "django_tables2/bootstrap.html"
        fields = ("record__student__roll_number",
                  'overall_attended', 'overall_total', 'percentage', 'status')
        row_attrs = {
            "style": lambda record: "background-color: #BBF7D0;" if record['status'] == "OK" else "background-color: #FEF08A;" if record['status'] == 'POOR' else "background-color: #FECACA;"}
