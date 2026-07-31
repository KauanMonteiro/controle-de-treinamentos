from django.shortcuts import render,redirect
from .forms import CompanyRegisterForm
from django.contrib.auth.decorators import login_required

@login_required
def register_company(request):
    form = CompanyRegisterForm(request.POST or None,user=request.user)

    if request.method == "POST":
        if form.is_valid():
            form.save()
            return redirect('home')
    return render(request,'pages/register_form.html',{'form':form})
