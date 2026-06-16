from .models import Profile
from django import forms

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = (
            'name',
            'email',
            'phone',
            'degree',
            'school',
            'university',
            'sumary',
            'previous_work',
            'skills',
        )
        labels = {
            'name': 'Nombre',
            'email': 'Correo electrónico',
            'phone': 'Teléfono',
            'degree': 'Grado',
            'school': 'Escuela',
            'university': 'Universidad',
            'sumary': 'Resumen',
            'previous_work': 'Experiencia previa',
            'skills': 'Habilidades',
        }
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'phone': forms.TextInput(attrs={'class': 'form-control'}),
            'degree': forms.TextInput(attrs={'class': 'form-control'}),
            'school': forms.TextInput(attrs={'class': 'form-control'}),
            'university': forms.TextInput(attrs={'class': 'form-control'}),
            'sumary': forms.Textarea(attrs={'class': 'form-control', 'rows': 5}),
            'previous_work': forms.Textarea(attrs={'class': 'form-control', 'rows': 5}),
            'skills': forms.TextInput(attrs={'class': 'form-control'}),
        }
        