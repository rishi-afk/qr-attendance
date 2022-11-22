from django.db import models
from django.contrib.auth import get_user_model
from django.contrib import admin
from django.core.exceptions import ValidationError
from django.forms import ModelForm
from dashboard.utils import validate_time_table
from smart_selects.db_fields import ChainedManyToManyField


class Course(models.Model):
    year = models.PositiveSmallIntegerField()
    title = models.CharField(max_length=30)

    def __str__(self) -> str:
        return f'{self.title} {self.year}'


class Professor(models.Model):
    user = models.OneToOneField(get_user_model(), on_delete=models.CASCADE)
    employee_id = models.CharField(max_length=50, unique=True)

    def __str__(self) -> str:
        return f'{self.user.username}'


class Paper(models.Model):
    code = models.CharField(max_length=20)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    professor = models.ForeignKey(Professor, on_delete=models.CASCADE)

    def __str__(self) -> str:
        return f'{self.code} - {self.professor}'


class Student(models.Model):
    user = models.OneToOneField(get_user_model(), on_delete=models.CASCADE)
    roll_number = models.CharField(max_length=20, unique=True)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)

    def __str__(self) -> str:
        return f'{self.roll_number}'


class Period(models.Model):
    paper = models.ForeignKey(Paper, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    start = models.TimeField()
    end = models.TimeField()

    def __str__(self) -> str:
        return f'{self.paper} | {self.start} - {self.end}'

    class Meta:
        constraints = [
            models.CheckConstraint(check=models.Q(
                end__gt=models.F("start")), name="check_end_time"),
            models.UniqueConstraint(
                fields=['paper', 'start', 'end'],
                name="unique_period_slot"
            ),
        ]


class TimeTable(models.Model):
    course = models.OneToOneField(Course, on_delete=models.CASCADE)
    monday = ChainedManyToManyField(
        Period,
        chained_field="course",
        chained_model_field="course",
        related_name="monday",
        blank=True
    )
    tuesday = ChainedManyToManyField(
        Period,
        chained_field="course",
        chained_model_field="course",
        related_name="tuesday",
        blank=True

    )
    wednesday = ChainedManyToManyField(
        Period,
        chained_field="course",
        chained_model_field="course",
        related_name="wednesday",
        blank=True
    )
    thursday = ChainedManyToManyField(
        Period,
        chained_field="course",
        chained_model_field="course",
        related_name="thursday",
        blank=True
    )
    friday = ChainedManyToManyField(
        Period,
        chained_field="course",
        chained_model_field="course",
        related_name="friday",
        blank=True
    )

    def __str__(self) -> str:
        return f'{self.course}'


class TimeTableForm(ModelForm):
    def clean(self):
        cleaned_data = super().clean()
        errors = validate_time_table(cleaned_data)
        if (len(errors)):
            raise ValidationError(
                'Multiple periods in same time slot on %(value)s',
                code='invalid',
                params={'value': ", ".join(errors)},
            )

    class Meta:
        model = TimeTable
        fields = '__all__'


class TimeTableAdmin(admin.ModelAdmin):
    form = TimeTableForm


class RecordAdmin(admin.ModelAdmin):
    readonly_fields = ("absent",)


class Record(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    date = models.DateField()
    entry_time = models.TimeField()
    exit_time = models.TimeField(null=True, blank=True)
    absent = models.BooleanField(default=False, blank=True)

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
    record = models.ForeignKey(Record, on_delete=models.CASCADE)
    paper = models.ForeignKey(Paper, on_delete=models.CASCADE)
    total = models.SmallIntegerField()
    attended = models.SmallIntegerField()

    def __str__(self) -> str:
        return f'{self.record}'
