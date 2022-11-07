from datetime import datetime, timedelta
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.db import transaction
import jwt
import pytz
from qr_attendance.settings import SECRET_KEY
from dashboard.models import Attendance, Paper
from .forms import StudentForm, UserForm
from .tables import AttendanceTable, AttendanceTableProfessor
from .forms import DateInputForm, DateStudentFilterForm
IST = pytz.timezone('Asia/Kolkata')


@login_required()
def home(request):
    if (request.user.is_superuser):
        return redirect("/admin")
    student = getattr(request.user, "student", None)
    if (student):
        now = datetime.now(IST)
        exp = now + timedelta(minutes=100)
        encoded_jwt = jwt.encode(
            {"id": request.user.id, "iat": now, "exp": exp}, SECRET_KEY, algorithm="HS256")
        papers = Paper.objects.filter(course=request.user.student.course)
        return render(request, 'home.html', {'qr_token': encoded_jwt, 'papers': papers})
    else:
        papers = Paper.objects.filter(professor=request.user.professor)
        return render(request, 'professor.html', {'papers': papers})


DAYS = {0: 'monday', 1: 'tuesday',
        2: 'wednesday', 3: 'thursday', 4: 'friday'}


@login_required()
def attendance(request, paper_id):
    if (request.user.is_superuser):
        return redirect("/admin")
    student = getattr(request.user, "student", None)
    if (student):
        if (request.method == "POST"):
            form = DateInputForm(request.POST)
            if (form.is_valid()):
                date = form.cleaned_data['date']
                if (date):
                    table = AttendanceTable(Attendance.objects.filter(
                        record__student__user__id=request.user.id, paper__id=paper_id, record__date=form.cleaned_data['date']))
                else:
                    table = AttendanceTable(Attendance.objects.filter(
                        record__student__user__id=request.user.id, paper__id=paper_id))
        else:
            form = DateInputForm()
            table = AttendanceTable(Attendance.objects.filter(
                record__student__user__id=request.user.id, paper__id=paper_id))
            return render(request, "attendance.html", {"table": table, 'form': form, 'paper_id': paper_id})
        return render(request, "attendance.html", {"table": table, 'form': form, 'paper_id': paper_id})
    else:
        if (request.method == "POST"):
            form = DateStudentFilterForm(request.POST)
            if (form.is_valid()):
                student = form.cleaned_data['student']
                date = form.cleaned_data['date']
                table = AttendanceTableProfessor(
                    Attendance.objects.filter(paper__id=paper_id, record__student=student, record__date=date))
        else:
            table = AttendanceTableProfessor(
                Attendance.objects.filter(paper__id=paper_id))
            form = DateStudentFilterForm()
            return render(request, "attendance.html", {"table": table, "form": form, 'paper_id': paper_id})
        return render(request, "attendance.html", {"table": table, "form": form, 'paper_id': paper_id})


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
