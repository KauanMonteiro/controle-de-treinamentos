from django.shortcuts import render,redirect
from .forms import CompanyRegisterForm, EditCompanyForm
from django.contrib.auth.decorators import login_required
from .models import Company
@login_required
def register_company(request):
    form = CompanyRegisterForm(request.POST or None,user=request.user)

    if request.method == "POST":
        if form.is_valid():
            form.save()
            return redirect('home')
    return render(request,'pages/register_form.html',{'form':form})

@login_required
def edit_company(request, company_id):
    company = Company.objects.get(id=company_id)
    form = EditCompanyForm(request.POST or None, instance=company, user=request.user)
    if request.method == "POST":
        if form.is_valid():
            form.save()
            return redirect('home')
    return render(request, 'pages/edit_company_form.html', {'form': form, 'company': company})


