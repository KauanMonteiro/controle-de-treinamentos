from django.shortcuts import render, redirect, get_object_or_404
from ..forms import RoleForm
from ..models import Role
from decorator import check_permissions

@check_permissions('cadastros')
def register_role(request):
    form = RoleForm(request.POST or None, user=request.user)

    if request.method == "POST" and form.is_valid():
        form.save()
        return redirect('employee:role_list')

    return render(request, 'pages/register_form.html', {'form': form})

@check_permissions('editar')
def edit_role(request, role_id):
    role = get_object_or_404(Role, id=role_id)

    form = RoleForm(
        request.POST or None,
        instance=role,
        user=request.user
    )

    if request.method == "POST" and form.is_valid():
        form.save()
        return redirect('employee:role_list')

    return render(request, 'pages/register_form.html', {'form': form})

@check_permissions('excluir')
def delete_role(request, role_id):
    role = get_object_or_404(Role, id=role_id)

    role.delete = True
    role.save()

    return redirect('employee:role_list')


def role_list(request):
    roles = Role.objects.filter(delete=False)

    return render(
        request,
        'pages/role_page.html',
        {'roles': roles}
    )