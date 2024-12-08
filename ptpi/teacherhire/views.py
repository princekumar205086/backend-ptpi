from django.shortcuts import render, get_object_or_404, redirect
from rest_framework.response import Response
from rest_framework import viewsets
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import User
from rest_framework.views import APIView
from django.contrib.auth import authenticate,login
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from rest_framework import status
from teacherhire.models import *
from teacherhire.serializers import *
from .authentication import ExpiringTokenAuthentication  
from datetime import timedelta, datetime
from rest_framework.decorators import action
from rest_framework.exceptions import AuthenticationFailed
from .permissions import IsRecruiterPermission, IsAdminPermission 
import uuid  
from .models import Level, Subject, Question, ClassCategory
from .serializers import QuestionSerializer

    
class RecruiterView(APIView):
    permission_classes = [IsRecruiterPermission]
    def get(self, request):
        return Response({"message": "You are a recruiter!"}, status=status.HTTP_200_OK)

class AdminView(APIView):
    permission_classes = [IsAdminPermission]

    def get(self, request):
        return Response({"message": "You are an admin!"}, status=status.HTTP_200_OK)


def check_for_duplicate(model_class, **kwargs):
    return model_class.objects.filter(**kwargs).exists()

def create_object(serializer_class, request_data, model_class):
    serializer = serializer_class(data=request_data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# for authenticated teacher
def create_auth_data(self, serializer_class, request_data, model_class, *args, **kwargs):
    if not self.request.user.is_authenticated:
        return Response(
            {'message': 'Authentication required to perform this action.'},
            status=status.HTTP_401_UNAUTHORIZED
        )
    serializer = serializer_class(data=request_data)
    if serializer.is_valid():
        serializer.save(user=self.request.user)  
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

def get_count(model_class):
    return model_class.objects.count()

class RegisterUser(APIView):
    def post(self, request):
        serializer = RegisterSerializer(data=request.data)

        if not serializer.is_valid():
            return Response({
                'status': 403,
                'error': serializer.errors,
                'message': 'Something went wrong'
            })
        
        serializer.save()
        user = CustomUser.objects.get(email=serializer.data['email'])
        token_obj, __ = Token.objects.get_or_create(user=user)

        return Response({
            'status': 200,
            'payload': serializer.data,
            'token': str(token_obj),
            'message': 'Your data is saved'
        })
    

def generate_refresh_token():
    return str(uuid.uuid4())

class LoginUser(APIView):
    def post(self, request):
        email = request.data.get('email')
        password = request.data.get('password')

        try:
            user = CustomUser.objects.get(email=email)
        except CustomUser.DoesNotExist:
            return Response({'message': 'Invalid email or password'}, status=status.HTTP_401_UNAUTHORIZED)

        if user.check_password(password):
            # Delete old token if it exists
            Token.objects.filter(user=user).delete()
            token = Token.objects.create(user=user)

            refresh_token = generate_refresh_token()
            roles = {
                'is_admin': user.is_staff,
                'is_recruiter': user.is_recruiter,
                'is_user': True
            }
            return Response({
                'access_token': token.key,
                'refresh_token': refresh_token,
                'username':user.username, 
                'email':user.email, 
                'roles': roles,
                # 'refresh_expires_at': refresh_expires_at,  
                'message': 'Login successful'
            }, status=status.HTTP_200_OK)
        else:
            return Response({'message': 'Invalid email or password'}, status=status.HTTP_401_UNAUTHORIZED)
            
class LogoutUser(APIView):
    authentication_classes = [ExpiringTokenAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            token = Token.objects.get(user=request.user)
            token.delete()
            return Response({"success": "Logout successful"}, status=status.HTTP_200_OK)
        except Token.DoesNotExist:
            return Response({"error": "Invalid or expired token"}, status=status.HTTP_400_BAD_REQUEST)

    
class UserProfileViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    authentication_classes = [ExpiringTokenAuthentication]   
    queryset = UserProfile.objects.all().select_related('user')
    serializer_class = UserProfileSerializer
    def create(self,request,*args, **kwargs):
        return create_auth_data(self, UserProfileSerializer, request.data,UserProfile)
    def get_queryset(self):
        user = self.request.user
        if user.is_authenticated:
            return UserProfile.objects.filter(user=self.request.user)
        else:
            return UserProfile.objects.none()
    
#TeacerAddress GET ,CREATE ,DELETE 
class TeachersAddressViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated,IsRecruiterPermission]
    authentication_classes = [ExpiringTokenAuthentication]
    serializer_class = TeachersAddressSerializer
    queryset = TeachersAddress.objects.all().select_related('user')

    def create(self, request, *args, **kwargs):
        print(f"User: {request.user}")
        return create_auth_data(self, TeachersAddressSerializer, request.data, TeachersAddress)

    @action(detail=False, methods=['get'])
    def count(self, request):
        print(f"User: {request.user}")
        count = get_count(TeachersAddress)
        return Response({"count": count})
    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.delete()
        return Response({"message": "TeacherAddress deleted successfully"}, status=status.HTTP_204_NO_CONTENT)
        
class SingleTeachersAddressViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    authentication_classes = [ExpiringTokenAuthentication] 
    serializer_class = TeachersAddressSerializer 
    queryset = TeachersAddress.objects.all().select_related('user')

    def create(self, request, *args, **kwargs):
        return create_auth_data(self, TeachersAddressSerializer, request.data, TeachersAddress)
    
    def get_queryset(self):
        return TeachersAddress.objects.filter(user=self.request.user)


class EducationalQulificationViewSet(viewsets.ModelViewSet):   
    permission_classes = [IsAuthenticated]    
    authentication_classes = [ExpiringTokenAuthentication] 
    serializer_class = EducationalQualificationSerializer 
    queryset = EducationalQualification.objects.all()

    def create(self, request):
        return create_object(EducationalQualificationSerializer, request.data, EducationalQualification)


    @action(detail=False, methods=['get'])
    def count(self, request):
        count = get_count(EducationalQualification)
        return Response({"count": count})
    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.delete()
        return Response({"message": "Educationqulification deleted successfully"}, status=status.HTTP_204_NO_CONTENT)
    
class LevelViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]    
    authentication_classes = [ExpiringTokenAuthentication]     
    queryset = Level.objects.all()
    serializer_class = LevelSerializer
    
    
    @action (detail=False,methods=['get'])
    def count(self):
        count = get_count(Level)
        return Response({"Count":count})
    
    @action(detail=True, methods=['get'], url_path='(subject/(?P<subject_id>[^/.]+)/)?(class-category/(?P<class_category_id>[^/.]+)/)?questions')
    def level_questions(self, request, pk=None, subject_id=None, class_category_id=None):
        """
        Custom action to fetch questions by level, optional subject, and optional class category.
        """
        try:
            level = Level.objects.get(pk=pk)
        except Level.DoesNotExist:
            return Response({"error": "Level not found"}, status=status.HTTP_404_NOT_FOUND)

        if subject_id:
            try:
                subject = Subject.objects.get(pk=subject_id)
            except Subject.DoesNotExist:
                return Response({"error": "Subject not found"}, status=status.HTTP_404_NOT_FOUND)
            questions = Question.objects.filter(level=level, subject=subject)
        else:
            questions = Question.objects.filter(level=level)

        if class_category_id:
            try:
                class_category = ClassCategory.objects.get(pk=class_category_id)
            except ClassCategory.DoesNotExist:
                return Response({"error": "Class Category not found"}, status=status.HTTP_404_NOT_FOUND)
            questions = questions.filter(class_category=class_category)
            
        serializer = QuestionSerializer(questions, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.delete()
        return Response({"message": "Level deleted successfully"}, status=status.HTTP_204_NO_CONTENT)

    
class SkillViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    authentication_classes = [ExpiringTokenAuthentication] 
    queryset = Skill.objects.all()
    serializer_class = SkillSerializer

    @action(detail=False, methods=['get'])
    def count(self, request):
        count = get_count(Skill)
        return Response({"Count": count})
    
    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.delete()
        return Response({"message": "Skill deleted successfully"}, status=status.HTTP_204_NO_CONTENT)
  
    
class TeacherSkillViewSet(viewsets.ModelViewSet):
    queryset = TeacherSkill.objects.all()
    permission_classes = [IsAuthenticated]
    authentication_classes = [ExpiringTokenAuthentication] 
    serializer_class = TeacherSkillSerializer
    
    def create(self, request, *args, **kwargs):
        return create_auth_data(self, TeacherSkillSerializer, request.data, TeacherSkill)
    @action(detail=False, methods=['get'])
    def count(self, request):
        count = get_count(TeacherSkill)
        return Response({"Count": count})
    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.delete()
        return Response({"message": "TeacherSkill deleted successfully"}, status=status.HTTP_204_NO_CONTENT)
    
class SingleTeacherSkillViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    authentication_classes = [ExpiringTokenAuthentication] 
    serializer_class = TeacherSkillSerializer
    
    def create(self, request, *args, **kwargs):
        return create_auth_data(self, TeacherSkillSerializer, request.data, TeacherSkill)
    
    def get_queryset(self):
        return TeacherSkill.objects.filter(user=self.request.user)
    
    
class SubjectViewSet(viewsets.ModelViewSet):    
    permission_classes = [IsAuthenticated] 
    authentication_classes = [ExpiringTokenAuthentication] 
    queryset = Subject.objects.all()
    serializer_class = SubjectSerializer
    
    @action (detail=False,methods=['get'])
    def count(self,request):
        count = get_count(Subject)
        return Response({"Count":count})
    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.delete()
        return Response({"message": "subject deleted successfully"}, status=status.HTTP_204_NO_CONTENT)
    
class TeacherViewSet(viewsets.ModelViewSet):    
    permission_classes = [IsAuthenticated]
    authentication_classes = [ExpiringTokenAuthentication] 
    queryset= Teacher.objects.all().select_related('user')
    serializer_class = TeacherSerializer

    def create(self,request):
        return create_object(TeacherSerializer,request.data,Teacher)
    
    @action (detail=False,methods=['get'])
    def count(self,request):
        count = get_count(Teacher)
        return Response({"Count":count})
    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.delete()
        return Response({"message": "Teacher deleted successfully"}, status=status.HTTP_204_NO_CONTENT)
    
class SingleTeacherViewSet(viewsets.ModelViewSet):    
    permission_classes = [IsAuthenticated]
    authentication_classes = [ExpiringTokenAuthentication] 
    serializer_class = TeacherSerializer

    def create(self,request,*args, **kwargs):
        return create_auth_data(self, TeacherSerializer, request.data, Teacher)
    def get_queryset(self):
        user = self.request.user
        if user.is_authenticated:
            return Teacher.objects.filter(user=self.request.user)
        else:
            return Teacher.objects.none()
    
    
    
class ClassCategoryViewSet(viewsets.ModelViewSet):    
    permission_classes = [IsAuthenticated]
    authentication_classes = [ExpiringTokenAuthentication] 
    queryset= ClassCategory.objects.all()
    serializer_class = ClassCategorySerializer

    def create(self,request):
        return create_object(ClassCategorySerializer,request.data,ClassCategory)
    
    @action (detail=False,methods=['get'])
    def count(self,request):
        count = get_count(ClassCategory)
        return Response({"Count":count})
    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.delete()
        return Response({"message": "ClassCategory deleted successfully"}, status=status.HTTP_204_NO_CONTENT)
    
    
class TeacherQualificationViewSet(viewsets.ModelViewSet): 
    permission_classes = [IsAuthenticated]
    authentication_classes = [ExpiringTokenAuthentication]
    queryset = TeacherQualification.objects.all()
    serializer_class = TeacherQualificationSerializer

    @action(detail=False, methods=['get'])
    def count(self, request):
        count = get_count(TeacherQualification)
        return Response({"count": count})
    def create(self, request, *args, **kwargs):
        return create_auth_data(self, TeacherQualificationSerializer, request.data, TeacherQualification)
    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.delete()
        return Response({"message": "Teacherqualification deleted successfully"}, status=status.HTTP_204_NO_CONTENT)
    
class SingleTeacherQualificationViewSet(viewsets.ModelViewSet): 
    permission_classes = [IsAuthenticated]
    authentication_classes = [ExpiringTokenAuthentication]
    queryset = TeacherQualification.objects.all()
    serializer_class = TeacherQualificationSerializer

    def create(self, request, *args, **kwargs):
        return create_auth_data(self, TeacherQualificationSerializer, request.data, TeacherQualification)
    def get_queryset(self):
        return TeacherQualification.objects.filter(user=self.request.user)
    
    
    
class TeacherExperiencesViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    authentication_classes = [ExpiringTokenAuthentication] 
    queryset = TeacherExperiences.objects.all()
    serializer_class = TeacherExperiencesSerializer

    def create(self,request,*args, **kwargs):
        return create_auth_data(self, TeacherExperiencesSerializer,request.data,TeacherExperiences)
   
    @action (detail=False,methods=['get'])
    def count(self,request):
        count = get_count(TeacherExperiences)
        return Response({"Count":count}) 
    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.delete()
        return Response({"message": "Teacherexperience deleted successfully"}, status=status.HTTP_204_NO_CONTENT)  

class SingleTeacherExperiencesViewSet(viewsets.ModelViewSet): 
    permission_classes = [IsAuthenticated]
    authentication_classes = [ExpiringTokenAuthentication]
    queryset = TeacherExperiences.objects.all()
    serializer_class = TeacherExperiencesSerializer

    def create(self, request, *args, **kwargs):
        return create_auth_data(self, TeacherExperiencesSerializer, request.data, TeacherExperiences)
    def get_queryset(self):
        return TeacherExperiences.objects.filter(user=self.request.user)
    
    
class QuestionViewSet(viewsets.ModelViewSet):
    queryset = Question.objects.all().select_related('subject', 'level')
    serializer_class = QuestionSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [ExpiringTokenAuthentication] 

    def create(self,request):
        return create_object(QuestionSerializer,request.data,Question)
    
    @action (detail=False,methods=['get'])
    def count(self,request):
        count = get_count(Question)
        return Response({"Count":count})
    
    # def get_queryset(self):
    #     queryset = Level.objects.all() def create(self, request, *args, **kwargs):
        request.data['user'] = request.user.id
        return super().create(request, *args, **kwargs)
    #     level_filter = self.request.query_params.get('level', None)
    #     if level_filter is not None:
    #         level_filter = int(level_filter)
    #         if level_filter == 1:
    #             queryset = queryset.filter(question__level=1)
    #         else:
    #             queryset = queryset.filter(question__level=level_filter)
    #     return queryset

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.delete()
        return Response({"message":" Question deleted successfully"}, status=status.HTTP_204_NO_CONTENT)

class RoleViewSet(viewsets.ModelViewSet):    
    permission_classes = [IsAuthenticated]
    authentication_classes = [ExpiringTokenAuthentication] 
    queryset= Role.objects.all()
    serializer_class = RoleSerializer
    def create(self,request):
        return create_object(RoleSerializer,request.data,Role)
    
    
    @action (detail=False,methods=['get'])
    def count(self,request):
        count = get_count(Role)
        return Response({"Count":count})
    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.delete()
        return Response({"message": "Role deleted successfully"}, status=status.HTTP_204_NO_CONTENT)

class PreferenceViewSet(viewsets.ModelViewSet):    
    permission_classes = [IsAuthenticated]
    authentication_classes = [ExpiringTokenAuthentication] 
    queryset= Preference.objects.all()
    serializer_class = PreferenceSerializer
    def create(self, request, *args, **kwargs):
        request.data['user'] = request.user.id
        return super().create(request, *args, **kwargs)
    def get_queryset(self):
        return Preference.objects.filter(user=self.request.user)
    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.delete()
        return Response({"message": "Prefernce deleted successfully"}, status=status.HTTP_204_NO_CONTENT)

class TeacherSubjectViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]    
    authentication_classes = [ExpiringTokenAuthentication]     
    queryset = TeacherSubject.objects.all()
    serializer_class = TeacherSubjectSerializer
    def create(self,request):
        return create_object(TeacherSubjectSerializer,request.data,TeacherSubject)
    
    @action (detail=False,methods=['get'])
    def count(self,request):
        count = get_count(TeacherSubject)
        return Response({"Count":count})
    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.delete()
        return Response({"message": "Teachersubject deleted successfully"}, status=status.HTTP_204_NO_CONTENT)
    
class SingleTeacherSubjectViewSet(viewsets.ModelViewSet): 
    permission_classes = [IsAuthenticated]
    authentication_classes = [ExpiringTokenAuthentication]
    queryset = TeacherSubject.objects.all()
    serializer_class = TeacherSubjectSerializer

    def create(self, request, *args, **kwargs):
        return create_auth_data(self, TeacherSubjectSerializer, request.data, TeacherSubject)
    def get_queryset(self):
        return TeacherSubject.objects.filter(user=self.request.user)
   

class TeacherClassCategoryViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]    
    authentication_classes = [ExpiringTokenAuthentication]     
    queryset = TeacherClassCategory.objects.all()
    serializer_class = TeacherClassCategorySerializer
    def create(self,request):
        return create_object(TeacherClassCategorySerializer,request.data,TeacherClassCategory)
    
    @action (detail=False,methods=['get'])
    def count(self,request):
        count = get_count(TeacherClassCategory)
        return Response({"Count":count})
    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.delete()
        return Response({"message": "Teacherclasscategory deleted successfully"}, status=status.HTTP_204_NO_CONTENT)

class TeacherExamResultViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]    
    authentication_classes = [ExpiringTokenAuthentication]     
    queryset = TeacherExamResult.objects.all()
    serializer_class = TeacherExamResultSerializer

    def create(self, request, *args, **kwargs):
        # Add the authenticated user to the request data
        data = request.data.copy()
        data['user'] = request.user.id  # Set user to the currently authenticated user

        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
        
    
    @action (detail=False,methods=['get'])
    def count(self,request):
        count = get_count(TeacherExamResult)
        return Response({"Count":count}) 
    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.delete()
        return Response({"message": "Teacxherexamresult deleted successfully"}, status=status.HTTP_204_NO_CONTENT)   

class JobPreferenceLocationViewSet(viewsets.ModelViewSet):    
    permission_classes = [IsAuthenticated]
    authentication_classes = [ExpiringTokenAuthentication] 
    queryset= JobPreferenceLocation.objects.all()
    serializer_class = JobPreferenceLocationSerializer

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.delete()
        return Response({"message": "Jobpreferencelocation deleted successfully"}, status=status.HTTP_204_NO_CONTENT)
    
    
    
class BasicProfileViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    authentication_classes = [ExpiringTokenAuthentication]
    queryset = BasicProfile.objects.all()
    serializer_class = BasicProfileSerializer

    def create(self, request, *args, **kwargs):
        data = request.data.copy()
        data['user'] = request.user.id
        serializer = self.get_serializer(data=data)
        if serializer.is_valid():
            self.perform_create(serializer)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
    def get_queryset(self):
        user = self.request.user
        if user.is_authenticated:
            return BasicProfile.objects.filter(user=user)
        else:
            return BasicProfile.objects.none()