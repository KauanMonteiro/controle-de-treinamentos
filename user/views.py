from django.shortcuts import render,redirect,reverse
from .forms import UserRegisterForm
from django.contrib.auth import authenticate, login
from decorator import check_permissions

def login_view(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(
            request,
            username=username,
            password=password
        )

        if user:
            login(request, user)
            return redirect('home')

    return render(request, 'pages/login.html')

def logout_view(request):
    request.session.flush()
    return redirect(reverse('home'))

@check_permissions('cadastros')
def register_view(request):
    form = UserRegisterForm(request.POST or None)
    if request.method == 'POST':
        if form.is_valid():
            form.save()
            return redirect('home') 
    return render(request, 'pages/register_form.html', {'form': form})    

def delete_user(request, user_id):
    pass