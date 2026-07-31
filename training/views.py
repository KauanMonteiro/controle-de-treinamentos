from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from company.models import Company
def home(request):
    companies = Company.objects.all()
    return render(request,'pages/home.html',{'companies':companies})