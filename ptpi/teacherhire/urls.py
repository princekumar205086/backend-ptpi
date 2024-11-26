from django.contrib import admin
from django.urls import path, include
from teacherhire.views import (
     RegisterUser,
    LoginUser,
    SkillViewSet,
    TeacherSkillViewSet, SkillCreateView, SkillDelete

    )
from rest_framework import routers

urlpatterns = [
    path('auth/',include('rest_framework.urls',namespace='rest_framework')),
    path('register/', RegisterUser.as_view(), name='register'),
    path('login/', LoginUser.as_view(), name='login'),    
    path('skill/', SkillViewSet.as_view({'get': 'list'}), name='skill'), 
    path('skill/create/', SkillCreateView.as_view(), name='skill-create'),    
    path('skill/<int:pk>/', SkillDelete.as_view(), name="skill-delete"),
    path('teacherSkill/', TeacherSkillViewSet.as_view({'get' : 'list'}), name='teacherskill'), 

]
