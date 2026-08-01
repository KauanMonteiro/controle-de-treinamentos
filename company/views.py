from django.shortcuts import render,redirect
from .forms import CompanyForm
from django.contrib.auth.decorators import login_required
from .models import Company
from employee.models import Employee
from decorator.check_permissions import check_permissions

@login_required
@check_permissions('cadastros')
def register_company(request):
    form = CompanyForm(request.POST or None,user=request.user)

    if request.method == "POST":
        if form.is_valid():
            form.save()
            return redirect('home')
    return render(request,'pages/register_form.html',{'form':form})

@login_required
@check_permissions('editar')
def edit_company(request, company_id):
    company = Company.objects.get(id=company_id)
    form = CompanyForm(request.POST or None, instance=company, user=request.user)
    if request.method == "POST":
        if form.is_valid():
            form.save()
            return redirect('home')
    return render(request,'pages/register_form.html',{'form':form})

@login_required
@check_permissions('excluir')
def delete_company(request, company_id):
    company = Company.objects.get(id=company_id)
    company.delete = True
    company.save()
    return redirect('home')

@login_required
def company_page(request, company_id):
    company = Company.objects.get(id=company_id)
    employees = Employee.objects.filter(company=company, delete=False)
    return render(request, 'pages/company_page.html', {'company': company, 'employees': employees})

