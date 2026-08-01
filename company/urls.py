from django.urls import path
from . import views
app_name = 'company'
urlpatterns = [
    path('register_company/', views.register_company, name='register_company'),
    path('edit_company/<int:company_id>/', views.edit_company, name='edit_company'),
    path('delete_company/<int:company_id>/', views.delete_company, name='delete_company'),
    path('company_page/<int:company_id>/', views.company_page, name='company_page'),
]