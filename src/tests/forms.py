from django import forms 
from .models import Test

class CreateForm(forms.Form):
    name = forms.CharField(max_length=120)
    deadline_date = forms.DateTimeField(widget=forms.DateTimeInput(attrs={'type': 'date'}))
    deadline_time = forms.TimeField(widget=forms.TimeInput(attrs={'type': 'time'}))
    client_timezone = forms.IntegerField(widget=forms.HiddenInput(attrs={'type':'hidden'}))