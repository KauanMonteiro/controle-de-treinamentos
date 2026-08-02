from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from django.http import HttpResponse
from company.models import Company
from employee.models import Employee
from .forms import TrainingRegisterForm, TrainingTypeForm, TrainingDocForm
from .models import TrainingRegister, TrainingType, TrainingDoc
import mimetypes
from django.views.decorators.clickjacking import xframe_options_exempt
from django.http import FileResponse
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
        return redirect('edit_training', employee_id=employee.id, training_type_id=training_type.id)

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

    training = TrainingRegister.objects.filter(
        employee=employee,
        training_type=training_type,
        delete=False
    ).first()

    if not training:
        messages.warning(
            request,
            'Nenhum treinamento encontrado para este funcionário e tipo. Por favor, crie um novo.'
        )
        return redirect('training_register_create', employee_id=employee.id, training_type_id=training_type.id)

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


@login_required
def upload_training_doc(request, employee_id):
    employee = get_object_or_404(Employee, pk=employee_id)

    if request.method == 'POST':
        form = TrainingDocForm(request.POST, request.FILES)
        if form.is_valid():
            training_doc = form.save(commit=False)
            training_doc.employee = employee
            training_doc.created_by = request.user
            training_doc.save()
            messages.success(request, 'Documento de treinamento enviado com sucesso.')
            return redirect('employee:employee_detail', employee_id=employee.id)
        messages.error(request, 'Corrija os erros abaixo.')
    else:
        form = TrainingDocForm()

    return render(
        request,
        'pages/register_form.html',
        {'form': form, 'employee': employee}
    )


@login_required
def view_training_docs(request, employee_id):
    employee = get_object_or_404(Employee, pk=employee_id)
    training_docs = TrainingDoc.objects.filter(employee=employee, delete=False)

    return render(
        request,
        'pages/training_docs_view.html',
        {'employee': employee, 'training_docs': training_docs}
    )


@login_required
def download_training_doc(request, doc_id):
    # CORRIGIDO: get_object_or_404 já retorna a instância certa;
    # não existe .filter() em cima dela (isso quebrava toda vez que era chamado).
    training_doc = get_object_or_404(TrainingDoc, pk=doc_id, delete=False)
    file_path = training_doc.docs.path

    with open(file_path, 'rb') as f:
        response = HttpResponse(f.read(), content_type='application/octet-stream')
        response['Content-Disposition'] = f'attachment; filename="{training_doc.docs.name}"'
        return response


@xframe_options_exempt
@login_required
def preview_training_doc(request, doc_id):
    training_doc = get_object_or_404(TrainingDoc, pk=doc_id, delete=False)

    content_type, _ = mimetypes.guess_type(training_doc.docs.name)
    content_type = content_type or 'application/octet-stream'

    response = FileResponse(
        training_doc.docs.open('rb'),
        content_type=content_type,
        filename=training_doc.docs.name,
    )
    response['Content-Disposition'] = f'inline; filename="{training_doc.docs.name}"'
    return response