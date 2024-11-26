from django.contrib import admin
from django.urls import path, include
from rest_framework.authtoken import views
from teacherhire.views import home, dashboard

urlpatterns = [

    # admin panel url
    path("home/", home),
    path("admin/dashboard/", dashboard, name='admin.dashboard'),
    path('admin/', admin.site.urls),
    path('api-token-auth/', views.obtain_auth_token),    
    path("api/",include('teacherhire.urls'))
]