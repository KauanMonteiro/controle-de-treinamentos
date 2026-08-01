from django.shortcuts import render,redirect
from .forms import CompanyForm
from django.contrib.auth.decorators import login_required
from .models import Company
@login_required
def register_company(request):
    form = CompanyForm(request.POST or None,user=request.user)

    if request.method == "POST":
        if form.is_valid():
            form.save()
            return redirect('home')
    return render(request,'pages/register_form.html',{'form':form})

@login_required
def edit_company(request, company_id):
    company = Company.objects.get(id=company_id)
    form = CompanyForm(request.POST or None, instance=company, user=request.user)
    if request.method == "POST":
        if form.is_valid():
            form.save()
            return redirect('home')
    return render(request,'pages/register_form.html',{'form':form})

@login_required
def delete_company(request, company_id):
    company = Company.objects.get(id=company_id)
    company.delete = True
    company.save()
    return redirect('home')


