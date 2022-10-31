from django.db import models
from django.contrib.auth.models import User
import pytz

IST = pytz.timezone('Asia/Kolkata')


class Course(models.Model):
    year = models.PositiveSmallIntegerField()
    title = models.CharField(max_length=30)

    def __str__(self) -> str:
        return f'{self.title} {self.year}'


class Professor(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    employee_id = models.CharField(max_length=50)

    def __str__(self) -> str:
        return f'{self.user.username}'


class Paper(models.Model):
    code = models.CharField(max_length=20)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    professor = models.ForeignKey(Professor, on_delete=models.CASCADE)

    def __str__(self) -> str:
        return f'{self.code} - {self.professor}'


class Student(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    roll_number = models.CharField(max_length=20, unique=True)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)

    def __str__(self) -> str:
        return f'{self.roll_number}'


class Period(models.Model):
    paper = models.OneToOneField(Paper, on_delete=models.CASCADE)
    start = models.TimeField()
    end = models.TimeField()

    def __str__(self) -> str:
        return f'{self.paper} | {self.start} - {self.end}'


class TimeTable(models.Model):
    course = models.OneToOneField(Course, on_delete=models.CASCADE)
    monday = models.ManyToManyField(
        Period, related_name="monday", blank=True)
    tuesday = models.ManyToManyField(
        Period, related_name="tuesday", blank=True)
    wednesday = models.ManyToManyField(
        Period, related_name="wednesday",  blank=True)
    thursday = models.ManyToManyField(
        Period, related_name="thursday",  blank=True)
    friday = models.ManyToManyField(
        Period, related_name="friday", blank=True)

    def __str__(self) -> str:
        return f'{self.course}'


class Record(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    date = models.DateField()
    entry_time = models.TimeField()
    exit_time = models.TimeField(null=True)

    def __str__(self) -> str:
        return f'{self.student} - {self.date}'

    class Meta:
        constraints = [
            models.CheckConstraint(check=models.Q(exit_time__isnull=True) | models.Q(
                exit_time__gt=models.F("entry_time")), name="check_exit_time"),
            models.UniqueConstraint(
                fields=['student', 'date'],
                name="student_entry_unique"
            ),
        ]


class Attendance(models.Model):
    record = models.OneToOneField(Record, on_delete=models.CASCADE)
    # period = models.ForeignKey(Period, on_delete=models.CASCADE)
    periods = models.ManyToManyField(Period)
