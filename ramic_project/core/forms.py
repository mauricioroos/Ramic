from django.contrib.auth.forms import UserCreationForm
from django import forms
from .models import Motor

class CustomUserCreationForm(UserCreationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs.update({'class': 'form-control'})
            if field_name == 'username':
                field.widget.attrs.update({'placeholder': 'Digite seu nome de usuário'})


class MotorForm(forms.ModelForm):
    class Meta:
        model = Motor
        fields = [
            'nome', 'modelo', 'numero_serie', 
            'corrente', 'potencia', 'tensao', 
            'localizacao', 'descricao', 'imagem'
        ]
        labels = {
            'nome': 'Nome do Motor',
            'numero_serie': 'Número Serial',
            'potencia': 'Potência (W)',
            'tensao': 'Tensão (V)',
            'corrente': 'Corrente (A)',
            'localizacao': 'Localização',
            'descricao': 'Descrição',
        }
        widgets = {
            'nome': forms.TextInput(attrs={'class': 'form-control'}),
            'modelo': forms.TextInput(attrs={'class': 'form-control'}),
            'numero_serie': forms.TextInput(attrs={'class': 'form-control'}),
            'corrente': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Ex: 6.8', 'step': '0.01'}),
            'potencia': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Ex: 1500'}),
            'tensao': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ex: 220V'}),
            'localizacao': forms.TextInput(attrs={'class': 'form-control'}),
            'descricao': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'imagem': forms.FileInput(attrs={'class': 'form-control'}),
        }