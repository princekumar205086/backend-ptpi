from django.contrib import admin
from .models import *

# Register your models here.

@admin.register(EducationalQualification)
class EducationalQualificationAdmin(admin.ModelAdmin):
    list_display = ['name', 'description']
@admin.register(TeacherQualification)
class TeacherQualificationAdmin(admin.ModelAdmin):
    list_display = ['user', 'qualification','institution','year_of_passing','grade_or_percentage']
@admin.register(TeacherExperiences)
class TeacherExperiencesAdmin(admin.ModelAdmin):
    list_display = ['user', 'role','institution','description','achievements','end_date','start_date']

@admin.register(Subject)
class SubjectAdmin(admin.ModelAdmin):
    list_display = ['subject_name','subject_description']

@admin.register(Role)
class RoleAdmin(admin.ModelAdmin):
    list_display = ['jobrole_name']

@admin.register(TeacherClassCategory)
class TeacherClassCategoryAdmin(admin.ModelAdmin):
    list_display = ['user', 'class_category']

# @admin.register(TeacherExamResult)
# class TeacherExamResultAdmin(admin.ModelAdmin):
#     list_display = ['user', 'subject', 'correct_answer', 'is_unanswered', 'incorrect_answer', 'isqualified', 'level', 'attempt']

# @admin.register(JobPreferenceLocation)
# class JobPreferenceLocationAdmin(admin.ModelAdmin):
#     list_display = ['preference', 'state', 'city', 'sub_division', 'block', 'area', 'pincode']

# @admin.register(UserProfile)
# class UserProfileAdmin(admin.ModelAdmin):
#     list_display = ['user', 'bio', 'profile_picture', 'phone_number', 'address', 'religion', 'hometown', 'pincode', 'date_of_birth', 'marital_status','gender', 'language']
    
