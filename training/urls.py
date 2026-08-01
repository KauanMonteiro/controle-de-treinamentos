from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('trainigs_view/', views.trainings_view, name='trainings_view'),
]