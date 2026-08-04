from django import forms
from django.forms import ModelForm
from django.contrib.auth.hashers import make_password
from .models import User


class UserRegisterForm(ModelForm):
    password = forms.CharField(
        label='Senha',
        widget=forms.PasswordInput(attrs={
            'placeholder': 'Deixe em branco para manter a senha atual'
        }),
        required=False,
    )

    class Meta:
        model = User
        fields = ['username', 'password', 'permissoes']
        widgets = {
            'permissoes': forms.CheckboxSelectMultiple,
        }

    def clean(self):
        cleaned_data = super().clean()
        username = cleaned_data.get('username')
        password = cleaned_data.get('password')

        if not username:
            self.add_error('username', 'Username is required.')

        # Senha só é obrigatória no cadastro (quando ainda não existe instance.pk)
        if not self.instance.pk and not password:
            self.add_error('password', 'Password is required.')

        return cleaned_data

    def save(self, commit=True):
        user = super().save(commit=False)
        user.username = self.cleaned_data['username']

        password = self.cleaned_data.get('password')
        if password:
            # Só re-hasheia se o usuário digitou uma senha nova
            user.password = make_password(password)
        # Se estiver em branco (edição), mantém o hash atual sem alterar

        if commit:
            user.save()
            self.save_m2m()  # necessário por causa do MultiSelectField 'permissoes'

        return user