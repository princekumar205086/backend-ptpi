from django.contrib import admin
from django.urls import path, include
from teacherhire.views import (
    RegisterUser, LoginUser, SubjectViewSet, SubjectCreateView,
    SubjectDeleteView, ClassCategoryViewSet, ClassCategoryCreateView,ClassCategoryDeleteView,
    RegisterUser, LoginUser,SubjectViewSet,SubjectCreateView, TeacherQualificationCreateView, TeacherExperiencesCreateView,
    SubjectDeleteView, TeacherExperiencesDeleteView, TeacherQualificationDeleteView,
     RegisterUser,
     RegisterUser,
    LoginUser
    )
from rest_framework import routers

urlpatterns = [
    path('auth/',include('rest_framework.urls',namespace='rest_framework')),
    path('register/', RegisterUser.as_view(), name='register'),
    path('login/', LoginUser.as_view(), name='login'),    
]