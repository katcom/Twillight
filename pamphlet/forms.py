from attr import field
from django import forms
from .models import *
class StatusEntryImageForm(forms.ModelForm):
    class Meta:
        model = StatusEntryImage
        fields=('status_entry','image_file')

class UserSettingForm(forms.ModelForm):
    class Meta:
        model = FacePamphletUser
        fields=('user_custom_name',)

class AvatarForm(forms.ModelForm):
    class Meta:
        model = AvatarEntry
        fields=('avatar_image',)