from django.shortcuts import render,redirect
from .forms import UserRegisterForm

def login_view(request):
    pass

def logout_view(request):
    pass

def register_view(request):
    form = UserRegisterForm(request.POST or None)
    if request.method == 'POST':
        if form.is_valid():
            form.save()
            return redirect('training:home') 
    return render(request, 'pages/register_form.html', {'form': form})    

def delete_user(request, user_id):
    pass