from django.urls import path
from . import views
app_name = 'user'
urlpatterns = [
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('edit_user/<int:user_id>/',views.edit_view, name='edit'),
    path('register/', views.register_view, name='register'),
    path('delete_user/<int:user_id>/', views.delete_user, name='delete_user'),
    path('user_page/',views.user_page, name='user_page')
]

