from django import forms
from django_summernote.widgets import SummernoteWidget

class MyForm(forms.Form):
    message = forms.CharField(widget=SummernoteWidget())