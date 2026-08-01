from django.db import models

class TrainingType(models.Model):
    name = models.CharField(max_length=100, verbose_name='Nome do Treinamento')
    codigo = models.CharField(max_length=20, unique=True, verbose_name='Código do Treinamento',null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey('user.User', on_delete=models.CASCADE)
    revision = models.IntegerField(default=1)

    def __str__(self):
        return self.name

class TrainingRegister(models.Model):
    effectiveness_choices = [
        ('E', 'Eficaz'),
        ('I', 'Não eficaz'),
    ]
    training_type = models.ForeignKey(TrainingType, on_delete=models.CASCADE, verbose_name='Tipo de Treinamento')
    employee = models.ForeignKey('employee.Employee', on_delete=models.CASCADE, verbose_name='Funcionário')
    docs = models.FileField(upload_to='training_docs/{employee_id.company.name}/{employee_id.name}/', null=True, blank=True)
    effectiveness = models.CharField(max_length=1, choices=effectiveness_choices, verbose_name='Eficácia')
    aplication_data_training = models.DateField(verbose_name='Data de Aplicação do Treinamento')
    instructor = models.CharField(max_length=100, verbose_name='Instrutor')
    evaluator = models.CharField(max_length=100, verbose_name='Avaliador')
    avaling_data_training = models.DateField(verbose_name='Data de Avaliação do Treinamento')
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey('user.User', on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.training_type.name} - {self.employee.name} - {self.employee.name}"
