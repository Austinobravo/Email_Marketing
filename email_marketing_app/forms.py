from django import forms

from django_summernote.widgets import SummernoteWidget
from .models import MyModel
class MyForm(forms.ModelForm):
    class Meta:
        model = MyModel
        fields = '__all__'
        widgets = {
            'message': SummernoteWidget(),
        }