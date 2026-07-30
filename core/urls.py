
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('user/', include('user.urls')),
    path('', include('training.urls')),
    path('employee/', include('employee.urls')),
    path('company/', include('company.urls')),
]
