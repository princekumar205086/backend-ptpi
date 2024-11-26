from django.contrib import admin
from django.urls import path, include
from teacherhire.views import (
    RegisterUser, LoginUser,SubjectViewSet,SubjectCreateView, TeacherQualificationCreateView, TeacherExperiencesCreateView,
    SubjectDeleteView, TeacherExperiencesDeleteView, TeacherQualificationDeleteView,
     RegisterUser,
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
    path('admin/skill/view/', SkillViewSet.as_view({'get': 'list'}), name='skill'), 
    path('admin/skill/create/', SkillCreateView.as_view(), name='skill-create'),    
    path('admin/skill/<int:pk>/', SkillDelete.as_view(), name="skill-delete"),
    path('teacherSkill/', TeacherSkillViewSet.as_view({'get' : 'list'}), name='teacherskill'), 
    path('admin/subject/view/', SubjectViewSet.as_view({'get': 'list'}), name='view-subject'),
    path('admin/subject/create/', SubjectCreateView.as_view(), name='subject-create'),
    path('admin/subject/<int:pk>/', SubjectDeleteView.as_view(), name='subject-delete'), 
    path('admin/teacherqualification/create/', TeacherQualificationCreateView.as_view(), name='teacherqualification-create'),
    path('admin/teacherQualification/<int:pk>/', TeacherQualificationDeleteView.as_view(), name='teacherQualification-delete'),  
    path('admin/teacherexperiences/create/',TeacherExperiencesCreateView.as_view(), name='teacherexperiences-create'),
    path('admin/teacherexperiences/<int:pk>/',TeacherExperiencesDeleteView.as_view(), name='teacherexperiences-delete'), 
    path('login/', LoginUser.as_view(), name='login'), 
    path('admin/subject/<int:pk>/', SubjectDeleteView.as_view(), name='subject-delete'),  
]
