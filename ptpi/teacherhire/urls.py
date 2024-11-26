from django.contrib import admin
from django.urls import path, include
from teacherhire.views import (
    RegisterUser, LoginUser, SubjectViewSet, SubjectCreateView,
    SubjectDeleteView, ClassCategoryViewSet, ClassCategoryCreateView,ClassCategoryDeleteView,
    RegisterUser, LoginUser,SubjectViewSet,SubjectCreateView, TeacherQualificationCreateView, TeacherExperiencesCreateView,
    SubjectDeleteView, TeacherExperiencesDeleteView, TeacherQualificationDeleteView,
     RegisterUser,
     RegisterUser,
    LoginUser,
    SkillViewSet,
    TeacherSkillViewSet, SkillCreateView, SkillDelete, LoginUser,SubjectViewSet,SubjectCreateView,
    SubjectDeleteView,
    TeacherQualificationViewSet, TeacherExperiencesViewSet,
    SkillViewSet,TeacherSkillViewSet, SkillCreateView, SkillDelete, 
    LoginUser,EducationalQulificationViewSet,TeachersAddressViewSet,TeachersAddressCreateView,EducationalQulificationCreateView
    )


urlpatterns = [
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
    #skill     
    path('admin/skill/view/', SkillViewSet.as_view({'get': 'list'}), name='skill'), 
    path('admin/skill/create/', SkillCreateView.as_view(), name='skill-create'),    
    path('admin/skill/<int:pk>/', SkillDelete.as_view(), name="skill-delete"),
    path('teacherSkill/', TeacherSkillViewSet.as_view({'get' : 'list'}), name='teacherskill'), 
    # teacherqualification
    path('admin/teacherqualification/create/', TeacherQualificationCreateView.as_view(), name='teacherqualification-create'),
    path('admin/teacherQualification/<int:pk>/', TeacherQualificationDeleteView.as_view(), name='teacherQualification-delete'),  
    path('admin/teacherexperiences/create/',TeacherExperiencesCreateView.as_view(), name='teacherexperiences-create'),
    path('admin/teacherexperiences/<int:pk>/',TeacherExperiencesDeleteView.as_view(), name='teacherexperiences-delete'), 
    path('login/', LoginUser.as_view(), name='login'),    
    path('edQulification/view/', EducationalQulificationViewSet.as_view({'get':'list'}), name='edQulification'),    
    path('edQulification/create/', EducationalQulificationCreateView.as_view(), name='edQulification-create'),
    path('teachersAddress/view/', TeachersAddressViewSet.as_view({'get':'list'}), name='teacherAddress'),    
    path('teachersAddress/create/', TeachersAddressCreateView.as_view(), name='teacherAddress-create'),    
]
