from django.contrib import admin
from django.urls import path, include
from teacherhire.views import (
    RegisterUser, LoginUser,SubjectViewSet,SubjectCreateView,
    SubjectDeleteView,ClassCategoryViewSet,ClassCategoryCreateView,ClassCategoryDeleteView,
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
    #subjects  
    path('admin/subject/view/', SubjectViewSet.as_view({'get': 'list'}), name='view-subject'),
    path('admin/subject/create/', SubjectCreateView.as_view(), name='subject-create'),
    path('admin/subject/<int:pk>/', SubjectDeleteView.as_view(), name='subject-delete'),
    #classcategory
    path('admin/classcategory/view/', ClassCategoryViewSet.as_view({'get': 'list'}), name='view-classcategory'),
    path('admin/classcategory/create/', ClassCategoryCreateView.as_view(), name='classcategory-create'),
    path('admin/classcategory/<int:pk>/', ClassCategoryDeleteView.as_view(), name='classcategory-delete'),  
    
]
