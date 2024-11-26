from django.contrib import admin
from django.urls import path, include
from teacherhire.views import (
     RegisterUser,
    LoginUser,EducationalQulificationViewSet,TeachersAddressViewSet
    )
from rest_framework import routers

urlpatterns = [
    path('auth/',include('rest_framework.urls',namespace='rest_framework')),
    path('register/', RegisterUser.as_view(), name='register'),
    path('login/', LoginUser.as_view(), name='login'),    
    path('edQulification/view/', EducationalQulificationViewSet.as_view({'get':'list'}), name='edQulification'),    
    path('teachersAddress/view/', TeachersAddressViewSet.as_view({'get':'list'}), name='teacherAddress'),    
]