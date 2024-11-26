from django.contrib import admin
from django.urls import path, include
from teacherhire.views import (
    RegisterUser, LoginUser,SubjectViewSet,SubjectCreateView, TeacherQualificationCreateView, TeacherExperiencesCreateView,
    SubjectDeleteView, TeacherExperiencesDeleteView, TeacherQualificationDeleteView,
     RegisterUser,
     RegisterUser,
    LoginUser
    )
from rest_framework import routers


router = routers.DefaultRouter()
#router.register(r'subjects',SubjectViewSet)
router.register(r"admin/teacherexperiences",TeacherExperiencesViewSet)
router.register(r"admin/teacherqualification",TeacherQualificationViewSet)
router.register(r"admin/skills",SkillViewSet)
router.register(r"admin/teacherskills",TeacherSkillViewSet),
router.register(r"admin/subjects",SubjectViewSet),




urlpatterns = [
    path('', include(router.urls)),
    path('auth/',include('rest_framework.urls',namespace='rest_framework')),
    path('register/', RegisterUser.as_view(), name='register'),
    path('login/', LoginUser.as_view(), name='login'),    
]