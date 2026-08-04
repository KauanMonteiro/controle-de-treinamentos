from django.shortcuts import render, redirect, reverse
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from .models import User
from .forms import UserRegisterForm
from decorator import check_permissions
from django.shortcuts import get_object_or_404

@check_permissions('cadastrar_usuario')
def user_page(request):
    user = User.objects.all()
    return render(request,'pages/user_page.html',{'user':user})

def login_view(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(
            request,
            username=username,
            password=password
        )

        if user is not None:
            login(request, user)
            messages.success(request, f'Bem-vindo(a), {user.get_full_name() or user.username}!')
            return redirect('home')

        messages.error(request, 'Usuário ou senha inválidos.')

    return render(request, 'pages/login.html')


def logout_view(request):
    logout(request)
    messages.success(request, 'Logout realizado com sucesso.')
    return redirect(reverse('home'))

@check_permissions('cadastrar_usuario')
def register_view(request):
    form = UserRegisterForm(request.POST or None,)

    if request.method == 'POST':
        if form.is_valid():
            form.save()
            messages.success(request, 'Usuário cadastrado com sucesso!')
            return redirect('home')
        else:
            messages.error(
                request,
                'Erro ao cadastrar o usuário. Verifique os campos informados.'
            )

    return render(
        request,
        'pages/register_form.html',
        {'form': form}
    )
@check_permissions('cadastrar_usuario')
def edit_view(request, user_id):
    user = get_object_or_404(User, id=user_id)
    form = UserRegisterForm(request.POST or None, instance=user)

    if request.method == 'POST':
        if form.is_valid():
            edited_user = form.save(commit=False)

            new_password = form.cleaned_data.get('password')

            if new_password:
                edited_user.set_password(new_password)
            else:
                edited_user.password = user.password

            edited_user.save()
            form.save_m2m() 
            messages.success(request, 'Usuário editado com sucesso!')
            return redirect('home')
        else:
            messages.error(
                request,
                'Erro ao editar o usuário. Verifique os campos informados.'
            )

    return render(
        request,
        'pages/register_form.html',
        {'form': form}
    )

def delete_user(request, user_id):
    if request.method == "POST":
        user = get_object_or_404(User, id=user_id)
        user.delete()
        messages.success(request, 'Usuário excluído com sucesso!')
    
    return redirect('home')
