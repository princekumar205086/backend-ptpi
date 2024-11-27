from django.shortcuts import render, get_object_or_404, redirect
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import viewsets
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth.models import User
from django.db import IntegrityError
from rest_framework.views import APIView
from django.contrib.auth import authenticate
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from rest_framework.exceptions import AuthenticationFailed
from rest_framework import viewsets
from teacherhire.models import (
    Subject,TeacherQualification, TeacherExperiences, Skill, TeacherSkill, Teacher,
    Subject,ClassCategory,TeacherQualification, TeacherExperiences,
    Skill, TeacherSkill, EducationalQualification,TeachersAddress,UserProfile)   
from teacherhire.serializers import (
    SubjectSerializer, ClassCategorySerializer, TeacherQualificationSerializer,
      TeacherExperiencesSerializer, UserSerializer,UserProfileSerializer, SkillSerializer, TeacherSkillSerializer,EducationalQualificationSerializer,TeachersAddressSerializer)
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated

def home(request):
  return render(request,"home.html")

def dashboard(request):
    return render(request, "admin_panel/dashboard.html")



class UserProfileViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset = UserProfile.objects.all().select_related('user')
    serializer_class = UserProfileSerializer

class TeachersAddressViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]    
    queryset = TeachersAddress.objects.select_related('user')
    serializer_class=TeachersAddressSerializer


class EducationalQulificationViewSet(viewsets.ModelViewSet):    
    permission_classes = [IsAuthenticated]
    queryset= EducationalQualification.objects.all()
    serializer_class=EducationalQualificationSerializer
    
class EducationalQulificationCreateView(APIView):
    permission_classes = [IsAuthenticated]
    def post(self, request):
        serializer = EducationalQualificationSerializer(data=request.data)        
        if serializer.is_valid():
            educationalQualification = serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)            

class TeachersAddressCreateView(APIView):
    def post(self,request):
        serializer = TeachersAddressSerializer(data=request.data)
        if serializer.is_valid():
            teachersAddress = serializer.save()
            return Response(serializer.data,status=status.HTTP_201_CREATED)
        return Response(serializer.data,status=status.HTTP_400_BAD_REQUEST)
        
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
        
# Skill GET method
class SkillViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset = Skill.objects.all()
    serializer_class = SkillSerializer

# Skill POST method
class SkillCreateView(APIView):
    def post(self, request):
        serializer = SkillSerializer(data=request.data)
        if serializer.is_valid():
            Skill = serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.data, status=status.HTTP_400_BAD_REQUEST)
    
# Skill DELETE method
class SkillDelete(APIView):
    def delete(self, request, pk):
        try:
            skill = Skill.objects.get(pk=pk)
            skill_name = skill.name
            skill.delete()
            return Response({"message": f"{skill_name} deleted successfuly"}, status= status.HTTP_204_NO_CONTENT)
        except Skill.DoesNotExist:
            return Response({"error" : "skill not found or unauthorized"}, status=status.HTTP_404_NOT_FOUND)


#Subject GET method
class SubjectViewSet(viewsets.ModelViewSet):    
    permission_classes = [IsAuthenticated]
    queryset= Subject.objects.all()
    serializer_class = SubjectSerializer

#Subject POST method
class SubjectCreateView(APIView):
    permission_classes = [IsAuthenticated]
    def post(self, request):
        serializer = SubjectSerializer(data=request.data)
        if serializer.is_valid():
            subject_name = serializer.validated_data.get("subject_name")
            if Subject.objects.filter(subject_name=subject_name).exists():
                return Response(
                    {"error": "Subject with this name already exists."},
                    status=status.HTTP_400_BAD_REQUEST
                )
            subject = serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)    
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
#Subject DELETE method
class SubjectDeleteView(APIView):
   permission_classes = [IsAuthenticated]
   def delete(self, request, pk):
        try:
            subject = Subject.objects.get(pk=pk)
            subject.delete()

            return Response({"message": "subject deleted successfully"}, status=status.HTTP_204_NO_CONTENT)
        except Subject.DoesNotExist:
            return Response({"error": "subject not found or unauthorized"}, status=status.HTTP_404_NOT_FOUND)

# Classcategory GET method
class ClassCategoryViewSet(viewsets.ModelViewSet):    
    permission_classes = [IsAuthenticated]
    queryset= ClassCategory.objects.all()
    serializer_class = ClassCategorySerializer

# Classcategory CREATE method
class ClassCategoryCreateView(APIView):
    permission_classes = [IsAuthenticated]
    def post(self, request):
        serializer = ClassCategorySerializer(data=request.data)
        if serializer.is_valid():
            name = serializer.validated_data.get("name")
            if ClassCategory.objects.filter(name=name).exists():
                return Response(
                    {"error": "ClassCategory with this name already exists."},
                    status=status.HTTP_400_BAD_REQUEST
                )
            subject = serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)    
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
# Classcategory DELETE method
class ClassCategoryDeleteView(APIView):
   permission_classes = [IsAuthenticated]
   def delete(self, request, pk):
        try:
            subject = ClassCategory.objects.get(pk=pk)
            subject.delete()

            return Response({"message": "classcategory deleted successfully"}, status=status.HTTP_204_NO_CONTENT)
        except ClassCategory.DoesNotExist:
            return Response({"error": "classcategory not found or unauthorized"}, status=status.HTTP_404_NOT_FOUND)

# TeacherQualification GET method
class TeacherQualificationViewSet(viewsets.ModelViewSet): 
    permission_classes = [IsAuthenticated]
    queryset = TeacherQualification.objects.all()

# TeacherQualification POST method
class TeacherQualificationCreateView(APIView):
    def post(self, request):
        serializer = TeacherQualificationSerializer(data=request.data)
        if serializer.is_valid():
            teacherqualification = serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)    
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
# TeacherQualification DELETE method
class TeacherQualificationDeleteView(APIView):
   def delete(self, request, pk):
        try:
            teacherQualification = TeacherQualification.objects.get(pk=pk)
            teacherQualification.delete()

            return Response({"message": "teacherQualification  deleted successfully"}, status=status.HTTP_204_NO_CONTENT)
        except TeacherQualification.DoesNotExist:
            return Response({"error": "teacherQualification  not found or unauthorized"}, status=status.HTTP_404_NOT_FOUND)
        
# TeacherExperiences GET method
class TeacherExperiencesViewSet(viewsets.ModelViewSet): 
    queryset = TeacherExperiences.objects.all()
    permission_classes = [IsAuthenticated]

# TeacherExperiences POST method
class TeacherExperiencesCreateView(APIView):
    def post(self, request):
        serializer = TeacherExperiencesSerializer(data=request.data)
        if serializer.is_valid():
            teacherexperiences = serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)    
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
# TeacherExperiences DELETE method
class TeacherExperiencesDeleteView(APIView):
   def delete(self, request, pk):
        try:
            teacherexperiences = TeacherExperiences.objects.get(pk=pk)
            teacherexperiences.delete()

            return Response({"message": "teacherexperiences  deleted successfully"}, status=status.HTTP_204_NO_CONTENT)
        except TeacherExperiences.DoesNotExist:
            return Response({"error": "teacherexperiences  not found or unauthorized"}, status=status.HTTP_404_NOT_FOUND)
        

# TeacherSkill GET  
class TeacherSkillViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset = TeacherSkill.objects.select_related('user','skill')
    serializer_class = TeacherSkillSerializer

# TeacherSkill POST
class TeacherSkillCreateView(APIView):
    def post(self, request):
        if not request.user.is_authenticated:
            return Response({"error": "User is not authenticated"}, status=status.HTTP_401_UNAUTHORIZED)
        
        if TeacherSkill.objects.filter(user=request.user).exists():
            return Response({"error": "Teacher profile already exists."}, status=status.HTTP_400_BAD_REQUEST)
        
        data = request.data.copy()
        data['user'] = request.user.id  

        serializer = TeacherSkillSerializer(data=data)
        if serializer.is_valid():
            try:
                teacherskill = serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)  
            except IntegrityError as e:
                return Response({"error": "Database integrity error", "details": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
# TeacherSkill DELETE
class TeacherSkillDeleteSet(APIView):
    def delete(self, request, pk):
        try:
            teacherskill = TeacherSkill.objects.get(pk=pk)
            user = teacherskill.user.username
            teacherskill.delete()
            return Response({"message": f"{user} TeacherSkill deleted successfuly"}, status=status.HTTP_204_NO_CONTENT)
        except TeacherSkill.DoesNotExist:
            return Response({"error": "TeacherSkill not found or unauthorized"}, status=status.HTTP_404_NOT_FOUND)
            
