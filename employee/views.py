from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required
from .forms import DepartmentForm, RoleForm, EmployeeForm
from .models import Department, Role, Employee


def register_department(request):
    form = DepartmentForm(request.POST or None, user=request.user)

    if request.method == "POST":
        if form.is_valid():
            form.save()
            return redirect('home')
    return render(request,'pages/register_form.html',{'form':form})

def register_role(request):
    form = RoleForm(request.POST or None, user=request.user)

    if request.method == "POST":
        if form.is_valid():
            form.save()
            return redirect('home')
    return render(request,'pages/register_form.html',{'form':form})

def register_employee(request):
    form = EmployeeForm(request.POST or None, user=request.user)

    if request.method == "POST":
        if form.is_valid():
            form.save()
            return redirect('home')
    return render(request,'pages/register_form.html',{'form':form})

def edit_department(request, department_id):
    department = Department.objects.get(id=department_id)
    form = DepartmentForm(request.POST or None, instance=department, user=request.user)

    if request.method == "POST":
        if form.is_valid():
            form.save()
            return redirect('home')
    return render(request,'pages/register_form.html',{'form':form})

def edit_role(request, role_id):
    role = Role.objects.get(id=role_id)
    form = RoleForm(request.POST or None, instance=role, user=request.user)

    if request.method == "POST":
        if form.is_valid():
            form.save()
            return redirect('home')
    return render(request,'pages/register_form.html',{'form':form})

def edit_employee(request, employee_id):
    employee = Employee.objects.get(id=employee_id)
    form = EmployeeForm(request.POST or None, instance=employee, user=request.user)

    if request.method == "POST":
        if form.is_valid():
            form.save()
            return redirect('home')
    return render(request,'pages/register_form.html',{'form':form})

def delete_department(request, department_id):
    department = Department.objects.get(id=department_id)
    department.delete = True
    department.save()
    return redirect(request.path) 

def delete_role(request, role_id):
    role = Role.objects.get(id=role_id)
    role.delete = True
    role.save()
    return redirect(request.path)

def delete_employee(request, employee_id):
    employee = Employee.objects.get(id=employee_id)
    employee.delete = True
    employee.save()
    return redirect(request.path)

