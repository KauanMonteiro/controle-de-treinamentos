from django.db import models

class Department(models.Model):
    name = models.CharField(max_length=100,verbose_name='Nome do Departamento')
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey('user.User', on_delete=models.CASCADE)
    delete = models.BooleanField(default=False)

    def __str__(self):
        return self.name

class Role(models.Model):
    name = models.CharField(max_length=100,verbose_name='Nome da Função')
    department = models.ForeignKey(Department, on_delete=models.CASCADE, verbose_name='Departamento')
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey('user.User', on_delete=models.CASCADE)
    delete = models.BooleanField(default=False)
 
    def __str__(self):
        return self.name


class Employee(models.Model):
    name = models.CharField(max_length=100,verbose_name='Nome do Funcionário')
    role = models.ForeignKey(Role, on_delete=models.CASCADE, verbose_name='Função')
    company = models.ForeignKey('company.Company', on_delete=models.CASCADE, verbose_name='Empresa')
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey('user.User', on_delete=models.CASCADE)
    delete = models.BooleanField(default=False)

    def __str__(self):
        return self.name