from .models import Profile
from django import forms

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['first_name', 'last_name', 'email', 'bio']