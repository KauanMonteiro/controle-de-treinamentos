from django.forms import ModelForm
from django.contrib.auth.hashers import make_password
from .models import User

class UserRegisterForm(ModelForm):
    class Meta:
        model = User
        fields = ['username', 'password']

    def clean(self):
        cleaned_data = super().clean()
        username = cleaned_data.get('username')
        password = cleaned_data.get('password')

        if not username:
            self.add_error('username', 'Username is required.')

        if not password:
            self.add_error('password', 'Password is required.')
        return cleaned_data
    def save(self, commit=True):
        user = super().save(commit=False)
        user.username = self.cleaned_data['username']
        user.password = make_password(self.cleaned_data['password'])

        if commit:
            user.save()

        return user


