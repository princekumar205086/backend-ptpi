from django.contrib import admin
from django.urls import path, include
from teacherhire.views import (
     RegisterUser,
    LoginUser,
    SkillViewSet,
    TeacherSkillViewSet, SkillCreateView, SkillDelete, LoginUser,SubjectViewSet,SubjectCreateView,
    SubjectDeleteView,
    TeacherQualificationViewSet, TeacherExperiencesViewSet,
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
    path('admin/skill/view/', SkillViewSet.as_view({'get': 'list'}), name='skill'), 
    path('admin/skill/create/', SkillCreateView.as_view(), name='skill-create'),    
    path('admin/skill/<int:pk>/', SkillDelete.as_view(), name="skill-delete"),
    path('teacherSkill/', TeacherSkillViewSet.as_view({'get' : 'list'}), name='teacherskill'), 
    path('admin/subject/view/', SubjectViewSet.as_view({'get': 'list'}), name='view-subject'),
    path('admin/subject/create/', SubjectCreateView.as_view(), name='subject-create'),
    path('admin/subject/<int:pk>/', SubjectDeleteView.as_view(), name='subject-delete'),  
]
