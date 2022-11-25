import jwt
from django.db.models import Sum, ExpressionWrapper, FloatField, F, When, Case, Value
from datetime import timedelta, datetime
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.db import transaction
from dashboard.models import Attendance, Paper
from dashboard.tables import AttendanceTable, AttendanceTableProfessor, AttendanceHistoryTable
from dashboard.forms import DateStudentFilterForm, StudentForm, UserForm, DateFilterForm
from django.conf import settings
from qr_attendance.settings import SECRET_KEY
from django_tables2.config import RequestConfig
from django_tables2.export.export import TableExport


@login_required()
def home(request):
    if (request.user.is_superuser):
        return redirect("/admin")
    student = getattr(request.user, "student", None)
    if (student):
        now = datetime.now(settings.IST)
        exp = now + timedelta(minutes=settings.AUTH_EXPIRY)
        encoded_jwt = jwt.encode(
            {"id": request.user.id, "iat": now, "exp": exp}, SECRET_KEY, algorithm="HS256")
        papers = Paper.objects.filter(course=student.course)
        return render(request, 'home.html', {'qr_token': encoded_jwt, 'papers': papers})
    else:
        papers = Paper.objects.filter(professor=request.user.professor)
        return render(request, 'professor.html', {'papers': papers})


@login_required()
def attendance(request, paper_id):
    if (request.user.is_superuser):
        return redirect("/admin")
    student = getattr(request.user, "student", None)
    if (student):
        paper_code = Paper.objects.get(id=paper_id).code
        form = DateFilterForm(request.GET)
        if (form.is_valid()):
            date = form.cleaned_data['date']
            if (date):
                table = AttendanceTable(Attendance.objects.filter(
                    record__student__user__id=request.user.id, paper__id=paper_id, record__date=date))
            else:
                table = AttendanceTable(Attendance.objects.filter(
                    record__student__user__id=request.user.id, paper__id=paper_id))
        else:
            table = AttendanceTable(Attendance.objects.filter(
                record__student__user__id=request.user.id, paper__id=paper_id))
            form = DateFilterForm()
        data = Attendance.objects.filter(
            record__student__user__id=request.user.id, paper__id=paper_id).aggregate(Sum('attended'), Sum('total'))
        attended_sum = data.get('attended__sum', 0) or 0
        total_sum = data.get('total__sum', 0) or 0
        return render(request, "attendance.html", {"table": table, 'enable_charts': True, 'paper_id': paper_id, "paper_code": paper_code, "form": form, 'data': [attended_sum, total_sum-attended_sum]})
    else:
        form = DateStudentFilterForm(request.GET)
        if (form.is_valid()):
            student = form.cleaned_data['student']
            date = form.cleaned_data['date']
            if (student and date):
                table = AttendanceHistoryTable(
                    Attendance.objects.filter(
                        paper__id=paper_id, record__student=student, record__date=date))
            elif (student):
                table = AttendanceHistoryTable(
                    Attendance.objects.filter(
                        paper__id=paper_id, record__student=student))
            elif (date):
                table = AttendanceHistoryTable(
                    Attendance.objects.filter(
                        paper__id=paper_id, record__date=date))
            else:
                table = AttendanceTableProfessor(
                    Attendance.objects.filter(
                        paper__id=paper_id).values(
                        'record__student__roll_number').order_by('record__student__roll_number').annotate(overall_total=Sum('total'), overall_attended=Sum('attended')).annotate(percentage=ExpressionWrapper(
                            F('overall_attended') * 100.0 / F('overall_total'),
                            output_field=FloatField()
                        )).annotate(status=Case(When(percentage__range=(75, 100), then=Value('OK')), When(percentage__range=(65, 75), then=Value('POOR')), default=Value('BAD'))))
                form = DateStudentFilterForm()
            RequestConfig(request).configure(table)
            export_format = request.GET.get("_export", None)
            if TableExport.is_valid_format(export_format):
                exporter = TableExport(export_format, table)
                return exporter.response("table.{}".format(export_format))
            return render(request, "attendance.html", {"table": table,  'enable_charts': False, "enable_download": True, "form": form, 'paper_id': paper_id})
        else:
            table = AttendanceTableProfessor(
                Attendance.objects.filter(
                    paper__id=paper_id).values(
                    'record__student__roll_number').order_by('record__student__roll_number').annotate(overall_total=Sum('total'), overall_attended=Sum('attended')).annotate(percentage=ExpressionWrapper(
                        F('overall_attended') * 100.0 / F('overall_total'),
                        output_field=FloatField()
                    )).annotate(status=Case(When(percentage__range=(75, 100), then=Value('OK')), When(percentage__range=(65, 75), then=Value('POOR')), default=Value('BAD'))))
            form = DateStudentFilterForm()
            RequestConfig(request).configure(table)
            export_format = request.GET.get("_export", None)
            if TableExport.is_valid_format(export_format):
                exporter = TableExport(export_format, table)
                return exporter.response("table.{}".format(export_format))
            return render(request, "attendance.html", {"table": table, "enable_download": True, 'enable_charts': False, "form": form, 'paper_id': paper_id})


@transaction.atomic
def register(response):
    if (response.user.is_authenticated):
        return redirect("/")

    if response.method == "POST":
        user_form = UserForm(response.POST)
        student_form = StudentForm(response.POST)

        if user_form.is_valid() and student_form.is_valid():
            user = user_form.save()
            user.refresh_from_db()
            student = student_form.save(commit=False)
            student.user = user
            student.save()
            return redirect("/")
    else:
        user_form = UserForm()
        student_form = StudentForm()

    return render(response, "auth/register.html", {"user_form": user_form, "student_form": student_form})
