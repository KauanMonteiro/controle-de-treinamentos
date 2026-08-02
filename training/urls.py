from django.urls import path

from . import views

urlpatterns = [
    path('', views.home, name='home'),

    # Tipos de treinamento
    path('trainings/', views.trainings_type_view, name='trainings_type_view'),
    path('trainings/register/', views.register_training_type, name='register_training_type'),
    path(
        'trainings/<int:training_type_id>/edit/',
        views.edit_training_type,
        name='edit_training_type',
    ),
    path(
        'trainings/<int:training_type_id>/delete/',
        views.delete_training_type,
        name='delete_training_type',
    ),

    # Registro de treinamento por funcionário
    path(
        'employee/<int:employee_id>/training/<int:training_type_id>/register/',
        views.training_register_create,
        name='training_register_create',
    ),
    path(
        'employee/<int:employee_id>/training/<int:training_type_id>/edit/',
        views.edit_training,
        name='edit_training',
    ),
    path(
        'employee/<int:employee_id>/training/<int:training_type_id>/delete/',
        views.delete_training,
        name='delete_training',
    ),
    path(
        'employee/<int:employee_id>/upload-doc/',
        views.upload_training_doc,
        name='upload_training_doc',
    ),

    path(
        'training-doc/<int:doc_id>/download/',
        views.download_training_doc,
        name='download_training_doc',
    ),

    # Preview inline do documento, usado pelo <iframe> em employee_detail.html
    path(
        'training-doc/<int:doc_id>/preview/',
        views.preview_training_doc,
        name='preview_training_doc',
    ),
]