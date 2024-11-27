from django.contrib import admin
from .models import EducationalQualification, TeacherQualification, TeacherExperiences, Subject

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
    
    
