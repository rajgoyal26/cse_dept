from .models import Faculty
from django import forms

class FacultyRegistrationForm(forms.ModelForm):
    class Meta:
        model=Faculty
        exclude=['user','submit']

class FacultyRegistrationFormSubmit(forms.ModelForm):
    class Meta:
        model=Faculty
        exclude=['department','date_of_join','date_of_leave','qualification','submit','user']
