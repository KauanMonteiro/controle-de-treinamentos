from django.shortcuts import render, redirect, get_object_or_404
from ..forms import EmployeeForm
from ..models import Employee
from decorator import check_permissions
from training.models import TrainingRegister

@check_permissions('cadastros')
def register_employee(request):
    form = EmployeeForm(
        request.POST or None,
        user=request.user
    )

    if request.method == "POST":
        if form.is_valid():
            form.save()
            return redirect('home')

    return render(
        request,
        'pages/register_form.html',
        {'form': form}
    )

@check_permissions('editar')
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
            return redirect('home')
    return render(
        request,
        'pages/register_form.html',
        {'form': form}
    )
@check_permissions('excluir')
def delete_employee(request, employee_id):
    employee = get_object_or_404(
        Employee,
        id=employee_id
    )
    employee.delete = True
    employee.save()
    return redirect(request.path)


def employee_detail(request, employee_id):
    employee = get_object_or_404(Employee, id=employee_id)
    trainings = employee.role.trainings.all()  # Tipos de treinamento do cargo

    # Para cada tipo de treinamento, busca o registro do funcionário (se existir)
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

    context = {
        'employee': employee,
        'trainings_with_registers': trainings_with_registers,
    }
    return render(request, 'pages/employee_detail.html', context)
