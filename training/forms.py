from django.forms import ModelForm, DateField, TextInput, ModelMultipleChoiceField, CheckboxSelectMultiple, ChoiceField, Select, CharField, Form
from .models import TrainingType, TrainingRegister, TrainingDoc

class TrainingTypeForm(ModelForm):
    class Meta:
        model = TrainingType
        fields = ['name', 'codigo', 'revision']
    def __init__(self, *args,user=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.user = user

    def clean(self):
        cleaned_data = super().clean()
        name = cleaned_data.get('name')
        codigo = cleaned_data.get('codigo')
        revision = cleaned_data.get('revision')
        if not name:
            self.add_error('name', 'Name is required.')
        if not codigo:
            self.add_error('codigo', 'Código is required.')
        return cleaned_data

    def save(self, commit=True):
        training_type = super().save(commit=False)
        training_type.name = self.cleaned_data['name']
        training_type.codigo = self.cleaned_data['codigo']
        training_type.revision = self.cleaned_data['revision']
        training_type.created_by = self.user
        if commit:
            training_type.save()
        return training_type

class TrainingRegisterForm(ModelForm):
    aplication_data_training = DateField(
        input_formats=['%d/%m/%Y', '%Y-%m-%d'],
        widget=TextInput(attrs={'class': 'form-control datepicker', 'placeholder': 'dd/mm/aaaa'})
    )
    avaling_data_training = DateField(
        input_formats=['%d/%m/%Y', '%Y-%m-%d'],
        widget=TextInput(attrs={'class': 'form-control datepicker', 'placeholder': 'dd/mm/aaaa'})
    )

    class Meta:
        model = TrainingRegister
        fields = ['effectiveness', 'aplication_data_training', 'instructor', 'evaluator', 'avaling_data_training']

    def __init__(self, *args, user=None, employee=None, training_type=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.user = user
        self.employee = employee
        self.training_type = training_type

    def clean(self):
        cleaned_data = super().clean()
        effectiveness = cleaned_data.get('effectiveness')
        aplication_data_training = cleaned_data.get('aplication_data_training')
        instructor = cleaned_data.get('instructor')
        evaluator = cleaned_data.get('evaluator')
        avaling_data_training = cleaned_data.get('avaling_data_training')

        if not effectiveness:
            self.add_error('effectiveness', 'Eficácia is required.')
        if not aplication_data_training:
            self.add_error('aplication_data_training', 'Data de Aplicação do Treinamento is required.')
        if not instructor:
            self.add_error('instructor', 'Instrutor is required.')
        if not evaluator:
            self.add_error('evaluator', 'Avaliador is required.')
        if not avaling_data_training:
            self.add_error('avaling_data_training', 'Data de Avaliação do Treinamento is required.')

        return cleaned_data

class TrainingDocForm(ModelForm):
    class Meta:
        model = TrainingDoc
        fields = ['docs']
    def __init__(self, *args, user=None, employee=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.user = user
        self.employee = employee

    def clean(self):
        cleaned_data = super().clean()
        docs = cleaned_data.get('docs')

        if not docs:
            self.add_error('docs', 'Documento is required.')

        return cleaned_data


class TrainingRegisterCreateForm(Form):
    training_types = ModelMultipleChoiceField(
        queryset=TrainingType.objects.filter(delete=False).order_by('name'),
        widget=CheckboxSelectMultiple(attrs={'class': 'form-check-input'}),
        label='Treinamentos realizados',
    )
    effectiveness = ChoiceField(
        choices=TrainingRegister.effectiveness_choices,
        label='Eficácia',
        widget=Select(attrs={'class': 'form-control'}),
    )
    aplication_data_training = DateField(
        input_formats=['%d/%m/%Y', '%Y-%m-%d'],
        widget=TextInput(attrs={'class': 'form-control datepicker', 'placeholder': 'dd/mm/aaaa'}),
        label='Data de Aplicação do Treinamento',
    )
    instructor = CharField(
        max_length=100,
        label='Instrutor',
        widget=TextInput(attrs={'class': 'form-control'}),
    )
    evaluator = CharField(
        max_length=100,
        label='Avaliador',
        required=False,
        widget=TextInput(attrs={'class': 'form-control'}),
    )
    avaling_data_training = DateField(
        input_formats=['%d/%m/%Y', '%Y-%m-%d'],
        required=False,
        widget=TextInput(attrs={'class': 'form-control datepicker', 'placeholder': 'dd/mm/aaaa'}),
        label='Data de Avaliação do Treinamento',
    )
 
    def __init__(self, *args, user=None, employee=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.user = user
        self.employee = employee
 
        # Pré-seleciona os treinamentos vinculados ao Role do colaborador.
        # No model Role, o M2M se chama `trainings` (não `training_types`).
        if employee is not None:
            role = getattr(employee, 'role', None)
            trainings_field = getattr(role, 'trainings', None)
            if trainings_field is not None:
                preselected_ids = list(trainings_field.values_list('id', flat=True))
                if not self.is_bound:
                    self.fields['training_types'].initial = preselected_ids
 
    def clean(self):
        cleaned_data = super().clean()
        if not cleaned_data.get('training_types'):
            self.add_error('training_types', 'Selecione ao menos um treinamento.')
        return cleaned_data
 
    def save(self, commit=True):
        """
        Cria um TrainingRegister para cada TrainingType selecionado.
        Retorna a lista de instâncias criadas.
        """
        registers = []
        for training_type in self.cleaned_data['training_types']:
            register = TrainingRegister(
                training_type=training_type,
                employee=self.employee,
                effectiveness=self.cleaned_data['effectiveness'],
                aplication_data_training=self.cleaned_data['aplication_data_training'],
                instructor=self.cleaned_data['instructor'],
                evaluator=self.cleaned_data['evaluator'],
                avaling_data_training=self.cleaned_data['avaling_data_training'],
                created_by=self.user,
            )
            if commit:
                register.save()
            registers.append(register)
        return registers
 
