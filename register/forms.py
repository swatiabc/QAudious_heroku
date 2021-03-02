from django import forms
from django.contrib.auth.models import User
from transcribe_audio.models import AudioDataModel
from models import *

class SignUpForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    
    class Meta:
        model = Dashboard
        fields = ('transcript','f_name','l_name','u_name','email','password')
        
