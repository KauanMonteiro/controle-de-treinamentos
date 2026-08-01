from django.shortcuts import render, redirect, get_object_or_404

from ..forms import EmployeeForm
from ..models import Employee


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


def delete_employee(request, employee_id):
    employee = get_object_or_404(
        Employee,
        id=employee_id
    )

    employee.delete = True
    employee.save()

    return redirect(request.path)