from django.contrib import admin

from dashboard.models import Attendance, Record, Period, Course, Paper, Professor, Student, TimeTable, TimeTableAdmin

admin.site.register(Course)
admin.site.register(Paper)
admin.site.register(Professor)
admin.site.register(Student)
admin.site.register(Period)
admin.site.register(TimeTable, TimeTableAdmin)
admin.site.register(Record)
admin.site.register(Attendance)
