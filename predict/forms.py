from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from predict.models import Heart, Liver
from .models import Profile

class UserRegisterForm(UserCreationForm):
    email = forms.EmailField(required=True, label='Email')
    first_name = forms.CharField(required=True, label='First Name')
    last_name = forms.CharField(required=True, label='Last Name')

    class Meta:
        model = User
        fields = ("first_name","last_name","username","email","password1","password2")

class UserUpdateForm(forms.ModelForm):
    email = forms.EmailField()
    first_name = forms.CharField()
    last_name = forms.CharField()

    class Meta:
        model = User
        fields = ("first_name","last_name","username","email")

class ProfileUpdateForm(forms.ModelForm):
    specialism = forms.CharField()
    address = forms.CharField()

    class Meta:
        model = Profile
        fields = ("image","specialism","address")

class LiverForm (forms.ModelForm):
    class Meta:
        model = Liver
        fields = "__all__"

class HeartForm (forms.ModelForm):
    class Meta:
        model = Heart
        fields = "__all__"