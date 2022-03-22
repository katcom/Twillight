from attr import field
from django import forms
from .models import *
from django.contrib.auth.forms import UserCreationForm
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

class RegisterForm(UserCreationForm):
	Nickname = forms.EmailField(required=True)

	class Meta:
		model = User
		fields = ("Nickname","username", "password1", "password2")

class LikeEntryForm(forms.ModelForm):
    class Meta:
        model = LikesEntry
        fields=('status',)