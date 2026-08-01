from django.contrib.auth.models import AbstractUser
from multiselectfield import MultiSelectField

PERMISSIONS = (
    ('cadastros', 'Cadastrar departamento, função, funcionário, treinamento e tipo de treinamento'),
    ('usuario', 'Cadastrar usuário'),
    ('editar', 'Editar departamento, função, funcionário, treinamento e tipo de treinamento'),
    ('excluir', 'Excluir departamento, função, funcionário, treinamento e tipo de treinamento'),
)

class User(AbstractUser):
    permissoes = MultiSelectField(
        choices=PERMISSIONS,
        blank=True,
        verbose_name='Permissões'
    )