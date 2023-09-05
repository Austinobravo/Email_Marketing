from django import forms
from ckeditor.fields import CKEditorWidget

class ContactForm(forms.Form):
    subject = forms.CharField(max_length=100)
    message = forms.CharField(
        widget=CKEditorWidget()
    )
