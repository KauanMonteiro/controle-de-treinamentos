from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages

from ..forms import EmployeeForm
from ..models import Employee
from decorator import check_permissions
from training.models import TrainingRegister, TrainingDoc


@check_permissions('cadastrar_funcionario')
def register_employee(request):
    form = EmployeeForm(
        request.POST or None,
        user=request.user
    )

    if request.method == "POST":
        if form.is_valid():
            form.save()
            messages.success(request, "Funcionário cadastrado com sucesso!")
            return redirect('home')
        else:
            messages.error(
                request,
                "Erro ao cadastrar o funcionário. Verifique os campos informados."
            )

    return render(
        request,
        'pages/register_form.html',
        {'form': form}
    )


@check_permissions('editar_funcionario')
def edit_employee(request, employee_id):
    employee = get_object_or_404(
        Employee,
        id=employee_id
    )

    form = EmployeeForm(
        request.POST or None,
        instance=employee,
        user=request.user
    )

    if request.method == "POST":
        if form.is_valid():
            form.save()
            messages.success(request, "Funcionário atualizado com sucesso!")
            return redirect('home')
        else:
            messages.error(
                request,
                "Erro ao atualizar o funcionário. Verifique os campos informados."
            )

    return render(
        request,
        'pages/register_form.html',
        {'form': form}
    )


@check_permissions('excluir_funcionario')
def delete_employee(request, employee_id):
    employee = get_object_or_404(
        Employee,
        id=employee_id
    )

    employee.delete = True
    employee.save()

    messages.success(request, "Funcionário excluído com sucesso!")

    return redirect(
        'company:company_page',
        company_id=employee.company.id
    )


def employee_detail(request, employee_id):
    employee = get_object_or_404(Employee, id=employee_id)

    trainings = employee.role.trainings.all()

    trainings_with_registers = []
    for training in trainings:
        register = TrainingRegister.objects.filter(
            employee=employee,
            training_type=training,
            delete=False
        ).first()

        trainings_with_registers.append({
            'training': training,
            'register': register,
        })

    training_doc = TrainingDoc.objects.filter(
        employee=employee,
        delete=False
    ).order_by('-id').first()

    context = {
        'employee': employee,
        'trainings_with_registers': trainings_with_registers,
        'training_doc': training_doc,
    }

    return render(
        request,
        'pages/employee_detail.html',
        context
    )
