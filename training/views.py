from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render

from company.models import Company
from employee.models import Employee

from .forms import TrainingRegisterForm, TrainingTypeForm
from .models import TrainingRegister, TrainingType


@login_required
def home(request):
    companies = Company.objects.filter(delete=False)
    return render(request, 'pages/home.html', {'companies': companies})


@login_required
def trainings_type_view(request):
    trainings = TrainingType.objects.filter(delete=False)
    return render(request, 'pages/trainings_type_view.html', {'trainings': trainings})


@login_required
def register_training_type(request):
    if request.method == 'POST':
        form = TrainingTypeForm(request.POST, user=request.user)
        if form.is_valid():
            training_type = form.save(commit=False)
            training_type.created_by = request.user
            training_type.save()
            messages.success(request, 'Tipo de treinamento registrado com sucesso.')
            return redirect('trainings_type_view')
        messages.error(request, 'Corrija os erros abaixo.')
    else:
        form = TrainingTypeForm(user=request.user)

    return render(request, 'pages/register_form.html', {'form': form})


@login_required
def edit_training_type(request, training_type_id):
    training_type = get_object_or_404(TrainingType, pk=training_type_id, delete=False)

    if request.method == 'POST':
        form = TrainingTypeForm(request.POST, instance=training_type, user=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Tipo de treinamento atualizado com sucesso.')
            return redirect('trainings_type_view')
        messages.error(request, 'Corrija os erros abaixo.')
    else:
        form = TrainingTypeForm(instance=training_type, user=request.user)

    return render(request, 'pages/register_form.html', {'form': form})


@login_required
def delete_training_type(request, training_type_id):
    training_type = get_object_or_404(TrainingType, pk=training_type_id, delete=False)
    training_type.delete = True
    training_type.save()
    messages.success(request, 'Tipo de treinamento excluído com sucesso.')
    return redirect('trainings_type_view')


@login_required
def training_register_create(request, employee_id, training_type_id):
    employee = get_object_or_404(Employee, pk=employee_id)
    training_type = get_object_or_404(TrainingType, pk=training_type_id, delete=False)

    # Verifica se já existe um treinamento para este funcionário e tipo
    existing_training = TrainingRegister.objects.filter(
        employee=employee,
        training_type=training_type,
        delete=False
    ).first()

    if existing_training:
        messages.info(
            request,
            'Já existe um treinamento registrado para este funcionário e tipo. Redirecionando para edição.'
        )
        # Redireciona para a view de edição (que usará o registro mais recente)
        return redirect('edit_training', employee_id=employee.id, training_type_id=training_type.id)

    # Se não existir, prossegue com a criação
    if request.method == 'POST':
        form = TrainingRegisterForm(
            request.POST,
            user=request.user,
            employee=employee,
            training_type=training_type,
        )
        if form.is_valid():
            training_register = form.save(commit=False)
            training_register.employee = employee
            training_register.training_type = training_type
            training_register.created_by = request.user
            training_register.save()
            messages.success(request, 'Treinamento registrado com sucesso.')
            return redirect('employee:employee_detail', employee_id=employee.id)
        messages.error(request, 'Corrija os erros abaixo.')
    else:
        form = TrainingRegisterForm(
            user=request.user,
            employee=employee,
            training_type=training_type,
        )

    return render(
        request,
        'pages/training_register_form.html',
        {'form': form, 'employee': employee, 'training_type': training_type}
    )

@login_required
def edit_training(request, employee_id, training_type_id):
    employee = get_object_or_404(Employee, pk=employee_id)
    training_type = get_object_or_404(TrainingType, pk=training_type_id, delete=False)

    # Busca o primeiro registro (evita DoesNotExist se não houver nenhum)
    training = TrainingRegister.objects.filter(
        employee=employee,
        training_type=training_type,
        delete=False
    ).first()

    # Se não existir, redireciona para a criação (ou exibe erro)
    if not training:
        messages.warning(
            request,
            'Nenhum treinamento encontrado para este funcionário e tipo. Por favor, crie um novo.'
        )
        return redirect('training_register_create', employee_id=employee.id, training_type_id=training_type.id)

    # Se existir, prossegue com a edição
    if request.method == 'POST':
        form = TrainingRegisterForm(
            request.POST,
            instance=training,
            user=request.user,
            employee=employee,
            training_type=training_type,
        )
        if form.is_valid():
            form.save()
            messages.success(request, 'Treinamento atualizado com sucesso.')
            return redirect('employee:employee_detail', employee_id=employee.id)
        messages.error(request, 'Corrija os erros abaixo.')
    else:
        form = TrainingRegisterForm(
            instance=training,
            user=request.user,
            employee=employee,
            training_type=training_type,
        )

    context = {
        'form': form,
        'employee': employee,
        'training_type': training_type,
    }
    return render(request, 'pages/training_register_form.html', context)


@login_required
def delete_training(request, employee_id, training_type_id):
    employee = get_object_or_404(Employee, pk=employee_id)
    training_type = get_object_or_404(TrainingType, pk=training_type_id)
    training = get_object_or_404(
        TrainingRegister,
        employee=employee,
        training_type=training_type,
        delete=False,
    )
    training.delete = True
    training.save()
    messages.success(request, 'Treinamento excluído com sucesso.')
    return redirect('employee:employee_detail', employee_id=employee.id)