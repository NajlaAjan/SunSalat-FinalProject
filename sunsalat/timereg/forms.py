from django import forms
from django.forms import ModelForm
from .models import Promise

class DateInput(forms.DateInput):
    input_type = 'date'

