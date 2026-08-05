from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages

from ..forms import EmployeeForm
from ..models import Employee, Role, Department
from decorator import check_permissions
from training.models import TrainingRegister, TrainingDoc
from django.db.models import Q
from django.http import JsonResponse
from training.models import TrainingType
from company.models import Company
@check_permissions('cadastrar_funcionario')
def register_employee(request, company_id):
    # Busca a empresa (você pode usar get_object_or_404)
    company = get_object_or_404(Company, pk=company_id)

    form = EmployeeForm(
        request.POST or None,
        user=request.user,
        initial={'company': company}  # pré-seleciona a empresa
    )

    if request.method == "POST":
        if form.is_valid():
            # Garante que a empresa salva seja a da URL
            employee = form.save(commit=False)
            employee.company = company
            employee.save()
            messages.success(request, "Funcionário cadastrado com sucesso!")
            return redirect('home')  # ou redirecione para a empresa
        else:
            messages.error(request, "Erro ao cadastrar. Verifique os campos.")

    return render(request, 'pages/register_form.html', {
        'form': form,
        'company': company,  # opcional, para exibir no template
    })


@check_permissions('editar_funcionario')
def edit_employee(request, employee_id):
    employee = get_object_or_404(
        Employee,
        id=employee_id
    )

    form = EmployeeForm(
        request.POST or None,
        instance=employee,
        user=request.user
    )

    if request.method == "POST":
        if form.is_valid():
            form.save()
            messages.success(request, "Funcionário atualizado com sucesso!")
            return redirect('home')
        else:
            messages.error(
                request,
                "Erro ao atualizar o funcionário. Verifique os campos informados."
            )

    return render(
        request,
        'pages/register_form.html',
        {'form': form}
    )


@check_permissions('excluir_funcionario')
def delete_employee(request, employee_id):
    employee = get_object_or_404(
        Employee,
        id=employee_id
    )

    employee.delete = True
    employee.save()

    messages.success(request, "Funcionário excluído com sucesso!")

    return redirect(
        'company:company_page',
        company_id=employee.company.id
    )


def employee_detail(request, employee_id):
    employee = get_object_or_404(Employee, id=employee_id)

    trainings = employee.role.trainings.all()

    trainings_with_registers = []
    for training in trainings:
        register = TrainingRegister.objects.filter(
            employee=employee,
            training_type=training,
            delete=False
        ).first()

        trainings_with_registers.append({
            'training': training,
            'register': register,
        })

    training_doc = TrainingDoc.objects.filter(
        employee=employee,
        delete=False
    ).order_by('-id').first()

    context = {
        'employee': employee,
        'trainings_with_registers': trainings_with_registers,
        'training_doc': training_doc,
    }

    return render(
        request,
        'pages/employee_detail.html',
        context
    )
def search(request):
    query = request.GET.get('q', '').strip()
    results = []
    if not query:
        return JsonResponse({'results': results})

    # Empresas (Company)
    companies = Company.objects.filter(
        Q(name__icontains=query) & Q(delete=False)
    )[:5]
    for c in companies:
        results.append({
            'type': 'company',
            'name': c.name,
            'url': f'/company/company_page/{c.id}/',   # ajuste conforme sua rota real
        })

    # Departamentos
    departments = Department.objects.filter(
        Q(name__icontains=query) & Q(delete=False)
    )[:5]
    for d in departments:
        results.append({
            'type': 'department',
            'name': d.name,
            'url': f'/employee/edit_department/{d.id}/',
        })

    # Funções (Roles)
    roles = Role.objects.filter(
        Q(name__icontains=query) & Q(delete=False)
    ).select_related('department')[:5]
    for r in roles:
        results.append({
            'type': 'role',
            'name': f'{r.name} ({r.department.name})',
            'url': f'/employee/edit_role/{r.id}/',
        })

    # Funcionários
    employees = Employee.objects.filter(
        Q(name__icontains=query) & Q(delete=False)
    ).select_related('role', 'company')[:5]
    for e in employees:
        results.append({
            'type': 'employee',
            'name': f'{e.name} — {e.role.name} ({e.company.name})',
            'url': f'/employee/employee_detail/{e.id}/',
        })

    # Tipos de treinamento
    trainings = TrainingType.objects.filter(
        Q(name__icontains=query) & Q(delete=False)
    )[:5]
    for t in trainings:
        results.append({
            'type': 'training_type',
            'name': f'{t.name} ({t.codigo or "sem código"})',
            'url': f'/training/trainings/{t.id}/edit/',
        })

    return JsonResponse({'results': results})