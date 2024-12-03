from django.contrib import admin
from django.urls import path, include
from teacherhire.views import *
from rest_framework import routers
#from .views import SubjectQuestionsView


router = routers.DefaultRouter()
router.register(r"teacher/teacherexperience",TeacherExperiencesViewSet)
router.register(r"teacher/teacherqualification",TeacherQualificationViewSet)
router.register(r"admin/skill",SkillViewSet)
router.register(r"teacher/teacherskill",TeacherSkillViewSet),
router.register(r"admin/subject",SubjectViewSet),
router.register(r"admin/classcategory",ClassCategoryViewSet),
router.register(r"admin/teacher",TeacherViewSet),
router.register(r'userprofiles', UserProfileViewSet),
router.register(r'admin/question', QuestionViewSet),
router.register(r'admin/educationalQulification', EducationalQulificationViewSet)
router.register(r'teacher/teachersAddress', TeachersAddressViewSet)
router.register(r'admin/level', LevelViewSet)
router.register(r'single/teacher', SingleTeacherViewSet, basename='single-teacher')

urlpatterns = [
    path('',include(router.urls)),
    path('auth/',include('rest_framework.urls',namespace='rest_framework')),
    path('register/', RegisterUser.as_view(), name='register'),
    path('login/', LoginUser.as_view()),
    path('logout/', LogoutUser.as_view()),
    #path('levels/<int:pk>/<int:subject_id>/questions/', SubjectQuestionsView.as_view(), name='subject-questions'),
]
