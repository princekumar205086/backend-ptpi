from django.contrib import admin
from django.urls import path, include
from rest_framework.authtoken import views
from teacherhire.views import home, dashboard

urlpatterns = [

    # admin panel url
    path("home/", home),
    path("admin/dashboard/", dashboard, name='admin.dashboard'),

    # Teachers
    # path("admin/manage/teacher/", manage_teacher, name='admin.manage.teacher'),
    # path("admin/<int:pk>/delete/teacher/", delete_teacher, name='admin.delete.teacher'),
    # path("admin/<int:pk>/edit/", edit_teacher, name='admin.edit.teacher'),

    # Subjects
    # path("admin/manage/subject/", manage_subject, name='admin.manage.subject'),
    # path("admin/<int:pk>/delete/subject/", delete_subject, name='admin.delete.subject'),

    # Qualification
    # path("admin/manage/qualification/", manage_qualification, name='admin.manage.qualification'),
    # path("admin/<int:pk>/delete/qualification/", delete_quali, name='admin.delete.qualification'),

    # Rating
    # path("admin/manage/rating/", manage_rating, name='admin.manage.rating'),
    # path("admin/<int:pk>/delete/rating/", delete_rating, name='admin.delete.rating'),

    # Question 
    # path("admin/manage/question/", manage_questions, name='admin.manage.question'),

    path('admin/', admin.site.urls),
    path('api-token-auth/', views.obtain_auth_token),    
    path("api/",include('teacherhire.urls'))
]
