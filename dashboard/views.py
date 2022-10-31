from datetime import datetime, timedelta, timezone
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

from qr_attendance.settings import SECRET_KEY
from .forms import StudentForm, UserForm
from django.db import transaction
import jwt

import pytz
IST = pytz.timezone('Asia/Kolkata')


@login_required()
def home(request):
    if (request.user.is_superuser):
        return redirect("/admin")
    now = datetime.now(IST)
    exp = now + timedelta(minutes=100)
    encoded_jwt = jwt.encode(
        {"id": request.user.id, "iat": now, "exp": exp}, SECRET_KEY, algorithm="HS256")
    return render(request, 'home.html', {'qr_token': encoded_jwt})


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
