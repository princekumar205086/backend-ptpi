from django.contrib import admin
from django.urls import path, include
from teacherhire.views import (
     RegisterUser, TeacherQualificationViewSet, TeacherExperiencesViewSet,
    LoginUser
    )
from rest_framework import routers
router = routers.DefaultRouter()
router.register(r"teacherQualifications",TeacherQualificationViewSet)
router.register(r"teacherExperiences",TeacherExperiencesViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('auth/',include('rest_framework.urls',namespace='rest_framework')),
    path('register/', RegisterUser.as_view(), name='register'),
    path('login/', LoginUser.as_view(), name='login'), 
]
