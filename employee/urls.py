from django.urls import path
from . import views
app_name = 'employee'
urlpatterns = [
    path('register_department/', views.register_department, name='register_department'),
    path('register_role/', views.register_role, name='register_role'),
    path('register_employee/', views.register_employee, name='register_employee'),
    path('edit_department/<int:department_id>/', views.edit_department, name='edit_department'),
    path('edit_role/<int:role_id>/', views.edit_role, name='edit_role'),
    path('edit_employee/<int:employee_id>/', views.edit_employee, name='edit_employee'),
    path('delete_department/<int:department_id>/', views.delete_department, name='delete_department'),
    path('delete_role/<int:role_id>/', views.delete_role, name='delete_role'),
    path('delete_employee/<int:employee_id>/', views.delete_employee, name='delete_employee'),
    path('list_departments/', views.list_departments, name='list_departments'),
    path('role_list/', views.role_list, name='role_list'),

]