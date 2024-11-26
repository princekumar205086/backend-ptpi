from django.contrib import admin
from django.urls import path, include
from teacherhire.views import (
    RegisterUser, LoginUser,SubjectViewSet,SubjectCreateView,
    SubjectDeleteView,
    )
from rest_framework import routers

urlpatterns = [
    path('auth/',include('rest_framework.urls',namespace='rest_framework')),
    path('register/', RegisterUser.as_view(), name='register'),
    path('login/', LoginUser.as_view(), name='login'),  
    path('admin/subject/view/', SubjectViewSet.as_view({'get': 'list'}), name='view-subject'),
    path('admin/subject/create/', SubjectCreateView.as_view(), name='subject-create'),
    path('admin/subject/<int:pk>/', SubjectDeleteView.as_view(), name='subject-delete'),  
]
