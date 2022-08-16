from django.forms import forms
from django.contrib.auth.models import User

class signupform(forms.Form):
    class Meta:
        model=User
        fields=['email','first_name','last_name','password','phone']

class loginform(forms.Form):
    class Meta:
        model=User
        fields=['username','password']