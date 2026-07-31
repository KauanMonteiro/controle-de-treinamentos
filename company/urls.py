from django.urls import path
from . import views
app_name = 'company'
urlpatterns = [
    path('register_company/', views.register_company, name='register_company'),
]