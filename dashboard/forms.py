from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms
from .models import Student


class UserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ["username", "password1", "password2"]


class StudentForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = ["roll_number", "course"]


class DateInputForm(forms.Form):
    date = forms.DateField(required=False, widget=forms.SelectDateWidget())


class DateStudentFilterForm(forms.Form):
    date = forms.DateField(required=False, widget=forms.SelectDateWidget())
    student = forms.ModelChoiceField(required=False,
                                     queryset=Student.objects.all())
