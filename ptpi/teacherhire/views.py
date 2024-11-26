from django.shortcuts import render, get_object_or_404, redirect
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import viewsets
from teacherhire.models import TeacherQualification, TeacherExperiences
from teacherhire.serializers import TeacherQualificationSerializer, TeacherExperiencesSerializer
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth.models import User
from teacherhire.serializers import UserSerializer
from django.db import IntegrityError
from django.contrib.auth import authenticate

from rest_framework import status
from rest_framework.exceptions import AuthenticationFailed


def home(request):
  return render(request,"home.html")

def dashboard(request):
    return render(request, "admin_panel/dashboard.html")


class RegisterUser(APIView):
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if not serializer.is_valid():
            return Response({
                'status': 400,
                'errors': serializer.errors,
                'message': 'Invalid data provided.'
            }, status=status.HTTP_400_BAD_REQUEST)

        try:
            user = serializer.save()
        except IntegrityError as e:
            if 'email' in str(e):
                return Response({
                    'status': 400,
                    'message': 'Email already exists.',
                    'errors': str(e)
                }, status=status.HTTP_400_BAD_REQUEST)
            elif 'username' in str(e):
                return Response({
                    'status': 400,
                    'message': 'Username already exists.',
                    'errors': str(e)
                }, status=status.HTTP_400_BAD_REQUEST)
            return Response({
                'status': 400,
                'message': 'Username or email already exists.',
                'errors': str(e)
            }, status=status.HTTP_400_BAD_REQUEST)

        refresh = RefreshToken.for_user(user)
        access_token = str(refresh.access_token)

        return Response({
            'status': 200,
            'payload': serializer.data,
            'token': access_token,
            'message': 'User registered successfully.'
        }, status=status.HTTP_201_CREATED)
               
class LoginUser(APIView):
    def post(self, request):        
        email = request.data.get("email")
        password = request.data.get("password")        
        if not email or not password:
            return Response({
                'status': 400,
                'message': 'Email and password are required.'
            }, status=status.HTTP_400_BAD_REQUEST)

        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return Response({
                'status': 401,
                'message': 'Invalid credentials, please try again.'
            }, status=status.HTTP_401_UNAUTHORIZED)
        if not user.is_active:
           raise AuthenticationFailed("Account is disabled, please contact support.")
       
        if user.check_password(password):
            refresh = RefreshToken.for_user(user)
            access_token = str(refresh.access_token)  

            # teacher_data = None

            # try:
            #     teacher = Teacher.objects.get(user=user)
            #     teacher_data = {
            #         'id': teacher.id,
            #         'user_id': teacher.user.id,
            #         'bio': teacher.bio,
            #         'experience_year': teacher.experience_year,
            #         'qualification': teacher.qualification,
            #         'subjects': [subject.title for subject in teacher.subject.all()], 
            #     }
            # except Teacher.DoesNotExist:
            #     teacher_data = None           

            return Response({
                'status': 200,                
                'message': 'Login successful.',
                'token': access_token,
                'refresh': str(refresh),
                'user': {
                    'id': user.id,
                    'email': user.email,
                    'username': user.username,
                },
                # 'teacher': teacher_data
            }, status=status.HTTP_200_OK)
        else:
            return Response({
                'status': 401,
                'message': 'Invalid credentials, please try again.'
            }, status=status.HTTP_401_UNAUTHORIZED)
        
class TeacherQualificationViewSet(viewsets.ModelViewSet): 
    queryset = TeacherQualification.objects.all()
    serializer_class=TeacherQualificationSerializer

class TeacherExperiencesViewSet(viewsets.ModelViewSet): 
    queryset = TeacherExperiences.objects.all()
    serializer_class=TeacherExperiencesSerializer
