from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages

from ..forms import DepartmentForm
from ..models import Department
from decorator import check_permissions


@check_permissions('cadastrar_departamento')
def register_department(request):
    form = DepartmentForm(request.POST or None, user=request.user)

    if request.method == "POST":
        if form.is_valid():
            form.save()
            messages.success(request, "Departamento cadastrado com sucesso!")
            return redirect('employee:list_departments')
        else:
            messages.error(request, "Erro ao cadastrar o departamento. Verifique os campos informados.")

    return render(
        request,
        'pages/register_form.html',
        {'form': form}
    )


@check_permissions('editar_departamento')
def edit_department(request, department_id):
    department = get_object_or_404(Department, id=department_id)

    form = DepartmentForm(
        request.POST or None,
        instance=department,
        user=request.user
    )

    if request.method == "POST":
        if form.is_valid():
            form.save()
            messages.success(request, "Departamento atualizado com sucesso!")
            return redirect('employee:list_departments')
        else:
            messages.error(request, "Erro ao atualizar o departamento. Verifique os campos informados.")

    return render(
        request,
        'pages/register_form.html',
        {'form': form}
    )


@check_permissions('excluir_departamento')
def delete_department(request, department_id):
    department = get_object_or_404(Department, id=department_id)

    department.delete = True
    department.save()

    messages.success(request, "Departamento excluído com sucesso!")

    return redirect('employee:list_departments')


def list_departments(request):
    departments = Department.objects.filter(delete=False)

    return render(
        request,
        'pages/department_page.html',
        {
            'departments': departments
        }
    )
