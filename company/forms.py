from django.forms import ModelForm
from .models import Company

class CompanyRegisterForm(ModelForm):
    class Meta():
        model = Company
        fields = ['name', 'cnpj']
    def __init__(self, *args, user=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.user = user
    def clean(self):
        cleaned_data = super().clean()
        name = cleaned_data.get('name')
        cnpj = cleaned_data.get('cnpj')
        if not name:
            self.add_error('name', 'Name is required.')
        if not cnpj:
            self.add_error('cnpj','cnpj is required.')
        return cleaned_data
    def save(self, commit = True):
        company = super().save(commit=False)
        company.name = self.cleaned_data['name']
        company.cnpj = self.cleaned_data['cnpj']
        company.created_by = self.user
        if commit:
            company.save()
        return company