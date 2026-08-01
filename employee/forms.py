from django.forms import ModelForm
from .models import Department, Role, Employee
from company.models import Company
class DepartmentForm(ModelForm):
    class Meta:
        model = Department
        fields = ['name']

    def __init__(self, *args, user=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.user = user

    def clean(self):
        cleaned_data = super().clean()
        name = cleaned_data.get('name')
        if not name:
            self.add_error('name', 'Name is required.')
        return cleaned_data

    def save(self, commit=True):
        department = super().save(commit=False)
        department.name = self.cleaned_data['name']
        department.created_by = self.user
        if commit:
            department.save()
        return department

class RoleForm(ModelForm):
    class Meta:
        model = Role
        fields = ['name', 'department']

    def __init__(self, *args, user=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.user = user

    def clean(self):
        cleaned_data = super().clean()
        name = cleaned_data.get('name')
        department = cleaned_data.get('department')
        if not name:
            self.add_error('name', 'Name is required.')
        if not department:
            self.add_error('department', 'Department is required.')
        return cleaned_data

    def save(self, commit=True):
        role = super().save(commit=False)
        role.name = self.cleaned_data['name']
        role.department = self.cleaned_data['department']
        role.created_by = self.user
        if commit:
            role.save()
        return role

class EmployeeForm(ModelForm):
    class Meta:
        model = Employee
        fields = ['name', 'role', 'company']

    def __init__(self, *args, user=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.user = user
        self.fields['company'].queryset = Company.objects.filter(delete=False)

    def clean(self):
        cleaned_data = super().clean()
        name = cleaned_data.get('name')
        role = cleaned_data.get('role')
        company = cleaned_data.get('company')
        if not name:
            self.add_error('name', 'Name is required.')
        if not role:
            self.add_error('role', 'Role is required.')
        if not company:
            self.add_error('company', 'Company is required.')
        return cleaned_data

    def save(self, commit=True):
        employee = super().save(commit=False)
        employee.name = self.cleaned_data['name']
        employee.role = self.cleaned_data['role']
        employee.company = self.cleaned_data['company']
        employee.created_by = self.user
        if commit:
            employee.save()
        return employee