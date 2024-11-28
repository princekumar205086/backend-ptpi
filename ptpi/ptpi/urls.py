from django.contrib import admin
from django.urls import path, include
from rest_framework.authtoken import views
from teacherhire.views import home, dashboard

urlpatterns = [
    path("home/", home),
    path('api-token-auth/', views.obtain_auth_token),    
    path("api/",include('teacherhire.urls'))
]