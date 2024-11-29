from django.contrib import admin
from django.urls import path, include
from teacherhire.views import *
from rest_framework import routers

router = routers.DefaultRouter()
router.register(r"admin/teacherexperience",TeacherExperiencesViewSet)
router.register(r"admin/teacherqualification",TeacherQualificationViewSet)
router.register(r"admin/skill",SkillViewSet)
router.register(r"admin/teacherskill",TeacherSkillViewSet),
router.register(r"admin/subject",SubjectViewSet),
router.register(r"admin/classcategory",ClassCategoryViewSet),
router.register(r"admin/teacher",TeacherViewSet),
router.register(r'userprofiles', UserProfileViewSet),
router.register(r'question', QuestionViewSet),
router.register(r'level', LevelView),
router.register(r'admin/educationalQulification', EducationalQulificationViewSet)
router.register(r'admin/teachersAddress', TeachersAddressViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('auth/',include('rest_framework.urls',namespace='rest_framework')),
    path('register/', RegisterUser.as_view(), name='register'),
    path('login/', LoginUser.as_view()),
    path('logout/', LogoutUser.as_view()),
]
