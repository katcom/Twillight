from attr import field
from django import forms
from .models import *
class StatusEntryImageForm(forms.ModelForm):
    class Meta:
        model = StatusEntryImage
        fields=('status_entry','image_file')