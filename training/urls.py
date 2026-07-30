from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('register_training/', views.register_training, name='register_training'),
]