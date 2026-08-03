from django.contrib.auth.models import AbstractUser
from multiselectfield import MultiSelectField

PERMISSIONS = (
    ('cadastrar_usuario', 'Cadastrar Usuário'),
    ('editar_usuario', 'Editar Usuário'),
    ('excluir_usuario', 'Excluir Usuário'),

    ('cadastrar_cargo', 'Cadastrar Cargo'),
    ('editar_cargo', 'Editar Cargo'),
    ('excluir_cargo', 'Excluir Cargo'),

    ('cadastrar_funcionario', 'Cadastrar Funcionário'),
    ('editar_funcionario', 'Editar Funcionário'),
    ('excluir_funcionario', 'Excluir Funcionário'),

    ('cadastrar_departamento', 'Cadastrar Departamento'),
    ('editar_departamento', 'Editar Departamento'),
    ('excluir_departamento', 'Excluir Departamento'),

    ('cadastrar_empresa', 'Cadastrar Empresa'),
    ('editar_empresa', 'Editar Empresa'),
    ('excluir_empresa', 'Excluir Empresa'),

    ('cadastrar_tipo_treinamento', 'Cadastrar Tipo de Treinamento'),
    ('editar_tipo_treinamento', 'Editar Tipo de Treinamento'),
    ('excluir_tipo_treinamento', 'Excluir Tipo de Treinamento'),

    ('cadastrar_treinamento', 'Cadastrar Treinamento'),
    ('editar_treinamento', 'Editar Treinamento'),
    ('excluir_treinamento', 'Excluir Treinamento'),

    ('cadastrar_documento_treinamento', 'Cadastrar ficha de Treinamento'),
    ('visualizar_documento_treinamento', 'Visualizar ficha de Treinamento'),

    ('gerar_pdf_treinamento', 'Gerar PDF de Treinamentos'),
)

class User(AbstractUser):
    permissoes = MultiSelectField(
        choices=PERMISSIONS,
        blank=True,
        verbose_name='Permissões'
    )