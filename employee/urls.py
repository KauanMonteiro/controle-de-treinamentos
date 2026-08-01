from django.urls import path
from . import views
app_name = 'employee'
urlpatterns = [
    path('register_department/', views.register_department, name='register_department'),
    path('register_role/', views.register_role, name='register_role'),
    path('register_employee/', views.register_employee, name='register_employee'),

]