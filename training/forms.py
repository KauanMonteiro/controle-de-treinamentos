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
        label='Treinamentos',
    )
    effectiveness = ChoiceField(
        choices=TrainingRegister.effectiveness_choices,
        label='Eficácia (padrão)',
        widget=Select(attrs={'class': 'form-control'}),
    )
    instructor = CharField(
        max_length=100,
        label='Instrutor (padrão)',
        widget=TextInput(attrs={'class': 'form-control'}),
    )
    evaluator = CharField(
        max_length=100,
        label='Avaliador (padrão)',
        required=False,
        widget=TextInput(attrs={'class': 'form-control'}),
    )
    aplication_data_training = DateField(
        input_formats=['%d/%m/%Y', '%Y-%m-%d'],
        widget=TextInput(attrs={'class': 'form-control datepicker', 'placeholder': 'dd/mm/aaaa'}),
        label='Data de Aplicação do Treinamento (padrão)',
    )
    avaling_data_training = DateField(
        input_formats=['%d/%m/%Y', '%Y-%m-%d'],
        required=False,
        widget=TextInput(attrs={'class': 'form-control datepicker', 'placeholder': 'dd/mm/aaaa'}),
        label='Data de Avaliação do Treinamento (padrão)',
    )

    def __init__(self, *args, user=None, employee=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.user = user
        self.employee = employee

        # NÃO exclui mais os já registrados — eles aparecem também,
        # só que em modo edição (condição tratada na view/template).
        queryset = TrainingType.objects.filter(delete=False).order_by('name')
        self.fields['training_types'].queryset = queryset

        if employee is not None and not self.is_bound:
            role = getattr(employee, 'role', None)
            trainings_field = getattr(role, 'trainings', None)
            already_registered_ids = set(
                TrainingRegister.objects.filter(
                    employee=employee, delete=False
                ).values_list('training_type_id', flat=True)
            )
            preselected_ids = already_registered_ids.copy()
            if trainings_field is not None:
                preselected_ids |= set(trainings_field.values_list('id', flat=True))
            self.fields['training_types'].initial = list(preselected_ids)

    def clean(self):
        cleaned_data = super().clean()
        if not cleaned_data.get('training_types'):
            self.add_error('training_types', 'Selecione ao menos um treinamento.')
        return cleaned_data

    def save(self, overrides, commit=True):
        """
        overrides: dict {training_type_id (int): {
            'effectiveness': str or None,
            'instructor': str or None,
            'evaluator': str or None,
            'aplication_data_training': date or None,
            'avaling_data_training': date or None,
        }}
        Para cada training_type marcado:
          - se já existir um TrainingRegister ativo para o funcionário -> ATUALIZA
          - senão -> CRIA
        """
        results = []
        existing_by_type = {
            r.training_type_id: r
            for r in TrainingRegister.objects.filter(employee=self.employee, delete=False)
        }

        for training_type in self.cleaned_data['training_types']:
            row = overrides.get(training_type.id, {})

            effectiveness = row.get('effectiveness') or self.cleaned_data['effectiveness']
            instructor = row.get('instructor') or self.cleaned_data['instructor']
            evaluator = row.get('evaluator') or self.cleaned_data.get('evaluator') or ''
            aplication_date = row.get('aplication_data_training') or self.cleaned_data['aplication_data_training']
            avaling_date = row.get('avaling_data_training') or self.cleaned_data.get('avaling_data_training')

            register = existing_by_type.get(training_type.id)

            if register:
                # CONDIÇÃO: já existe -> edita o registro existente
                register.effectiveness = effectiveness
                register.instructor = instructor
                register.evaluator = evaluator
                register.aplication_data_training = aplication_date
                register.avaling_data_training = avaling_date
            else:
                # CONDIÇÃO: não existe -> cria novo
                register = TrainingRegister(
                    training_type=training_type,
                    employee=self.employee,
                    effectiveness=effectiveness,
                    aplication_data_training=aplication_date,
                    instructor=instructor,
                    evaluator=evaluator,
                    avaling_data_training=avaling_date,
                    created_by=self.user,
                )

            if commit:
                register.save()
            results.append(register)
        return results
 
