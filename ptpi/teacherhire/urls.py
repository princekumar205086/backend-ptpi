from django.contrib import admin
from django.urls import path, include
from teacherhire.views import (
    RegisterUser, LoginUser, SubjectViewSet, SubjectCreateView,
    SubjectDeleteView, ClassCategoryViewSet, ClassCategoryCreateView,ClassCategoryDeleteView,
     TeacherQualificationCreateView, TeacherExperiencesCreateView,
     TeacherExperiencesDeleteView, TeacherQualificationDeleteView,
    EducationalQulificationViewSet,TeachersAddressViewSet,TeachersAddressCreateView,EducationalQulificationCreateView
,TeacherQualificationViewSet,TeacherExperiencesViewSet,SkillViewSet,TeacherSkillViewSet,SkillCreateView,SkillDelete,
    SubjectDeleteView, ClassCategoryViewSet, ClassCategoryCreateView,ClassCategoryDeleteView, 
    LoginUser,SubjectViewSet,SubjectCreateView, TeacherQualificationCreateView, 
    TeacherExperiencesCreateView,
    SubjectDeleteView, TeacherExperiencesDeleteView, TeacherQualificationDeleteView,
    SkillViewSet,
    TeacherSkillViewSet, SkillCreateView, SkillDelete,SubjectViewSet,SubjectCreateView,
    TeacherQualificationViewSet, TeacherExperiencesViewSet,TeacherSkillCreateView,TeacherSkillDeleteSet,
    EducationalQulificationViewSet,TeachersAddressViewSet,UserProfileViewSet,TeachersAddressCreateView,EducationalQulificationCreateView,
    )
from rest_framework import routers


router = routers.DefaultRouter()
router.register(r"admin/teacherexperiences",TeacherExperiencesViewSet)
router.register(r"admin/teacherqualification",TeacherQualificationViewSet)
router.register(r"admin/skills",SkillViewSet)
router.register(r"admin/educationqulification",EducationalQulificationViewSet)
router.register(r"admin/classcategory",ClassCategoryViewSet)
router.register(r"admin/teacheraddress",TeachersAddressViewSet)
router.register(r"admin/teacherskills",TeacherSkillViewSet)
router.register(r"admin/subjects",SubjectViewSet)



router.register(r"admin/teacherskills",TeacherSkillViewSet),
router.register(r"admin/subjects",SubjectViewSet),
router.register(r'userprofiles', UserProfileViewSet)

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
    #skill     
    path('admin/skill/view/', SkillViewSet.as_view({'get': 'list'}), name='skill'), 
    path('admin/skill/create/', SkillCreateView.as_view(), name='skill-create'),    
    path('admin/skill/<int:pk>/', SkillDelete.as_view(), name="skill-delete"),
    path('teacherSkill/', TeacherSkillViewSet.as_view({'get' : 'list'}), name='teacherskill'), 
    # teacherqualification
    path('admin/teacherqualification/create/', TeacherQualificationCreateView.as_view(), name='teacherqualification-create'),
    path('admin/teacherQualification/view/', TeacherQualificationViewSet.as_view({'get': 'list'}), name='view-teacherQualification'),
    path('admin/teacherQualification/<int:pk>/', TeacherQualificationDeleteView.as_view(), name='teacherQualification-delete'),

    # teacherexperiences  
    path('admin/teacherexperiences/create/',TeacherExperiencesCreateView.as_view(), name='teacherexperiences-create'),
    path('admin/teacherexperiences/view/', TeacherExperiencesViewSet.as_view({'get': 'list'}), name='view-teacherexperiences'),
    path('admin/teacherexperiences/<int:pk>/',TeacherExperiencesDeleteView.as_view(), name='teacherexperiences-delete'),

    path('edQulification/view/', EducationalQulificationViewSet.as_view({'get':'list'}), name='edQulification'),    
    path('edQulification/create/', EducationalQulificationCreateView.as_view(), name='edQulification-create'),
    path('teachersAddress/view/', TeachersAddressViewSet.as_view({'get':'list'}), name='teacherAddress'),    
    path('teachersAddress/create/', TeachersAddressCreateView.as_view(), name='teacherAddress-create'),    
]
