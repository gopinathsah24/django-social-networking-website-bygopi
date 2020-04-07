
from django import forms
from . models import Profile
from accounts.models import User
class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields  = ["profile_image",
    "cover_image", 
    "phone","city",
    "country" 
        ]


class UserUpdateForm(forms.ModelForm):
    
    
    class Meta:
        model = User
        fields = [ 'firstname','lastname','gender','about']