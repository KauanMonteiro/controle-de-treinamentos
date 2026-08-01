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