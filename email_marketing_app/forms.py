from django import forms
from ckeditor.fields import CKEditorWidget

class ContactForm(forms.Form):
    subject = forms.CharField(max_length=100)
    message = forms.CharField(
        widget=CKEditorWidget()
    )
from django_summernote.widgets import SummernoteWidget

class MyForm(forms.Form):
    message = forms.CharField(widget=SummernoteWidget())