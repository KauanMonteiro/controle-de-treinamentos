from django.shortcuts import render, redirect, get_object_or_404
from ..forms import DepartmentForm
from ..models import Department
from decorator import check_permissions

@check_permissions('cadastros')
def register_department(request):
    form = DepartmentForm(request.POST or None, user=request.user)

    if request.method == "POST" and form.is_valid():
        form.save()
        return redirect('employee:list_departments')

    return render(request, 'pages/register_form.html', {'form': form})

@check_permissions('editar')
def edit_department(request, department_id):
    department = get_object_or_404(Department, id=department_id)

    form = DepartmentForm(
        request.POST or None,
        instance=department,
        user=request.user
    )

    if request.method == "POST" and form.is_valid():
        form.save()
        return redirect('employee:list_departments')

    return render(request, 'pages/register_form.html', {'form': form})

@check_permissions('excluir')
def delete_department(request, department_id):
    department = get_object_or_404(Department, id=department_id)
    department.delete = True
    department.save()

    return redirect('employee:list_departments')


def list_departments(request):
    departments = Department.objects.filter(delete=False)

    return render(
        request,
        'pages/department_page.html',
        {'departments': departments}
    )