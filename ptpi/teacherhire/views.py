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
import uuid  

# fuctions
def check_for_duplicate(model_class, **kwargs):

    return model_class.objects.filter(**kwargs).exists()

def create_object(serializer_class, request_data, model_class):

    serializer = serializer_class(data=request_data)
    if serializer.is_valid():
        if check_for_duplicate(model_class, **serializer.validated_data):
            return Response(
                {'message': f'Duplicate entry: {model_class.__name__} already exists.'},
                status=status.HTTP_400_BAD_REQUEST
            )
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

def delete_object(model_class, pk):
    try:
        instance = model_class.objects.get(pk=pk)
        instance.delete()
        return Response({"message": f"{model_class.__name__} deleted successfully"}, status=status.HTTP_204_NO_CONTENT)
    except model_class.DoesNotExist:
        return Response({"message": f"{model_class.__name__} not found"}, status=status.HTTP_404_NOT_FOUND)

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
        user = User.objects.get(email=serializer.data['email'])
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
            # Find the user by email
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return Response({'message': 'Invalid email or password'}, status=status.HTTP_401_UNAUTHORIZED)

        # Check if the password is correct
        if user.check_password(password):
            # Delete old token if it exists
            Token.objects.filter(user=user).delete()
            token = Token.objects.create(user=user)

            refresh_token = generate_refresh_token()

            return Response({
                'access_token': token.key,
                'refresh_token': refresh_token,
                'username':user.username, 
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

    @action(detail=False, methods=['get'])
    def count(self, request):
        count = self.get_queryset().count()
        return Response({"count": count})

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.delete()
        return Response({"message": "UserProfile deleted successfully"}, status=status.HTTP_204_NO_CONTENT)

#TeacerAddress GET ,CREATE ,DELETE 
class TeachersAddressViewSet(viewsets.ModelViewSet):
    serializer_class = TeachersAddressSerializer 
    queryset = TeachersAddress.objects.all().select_related('user')

    def create(self, request):
        return create_object(TeachersAddressSerializer, request.data, TeachersAddress)

    def destroy(self, request, pk=None):
        return delete_object(TeachersAddress, pk)

    @action(detail=False, methods=['get'])
    def count(self, request):
        count = get_count(TeachersAddress)
        return Response({"count": count})

class EducationalQulificationViewSet(viewsets.ModelViewSet):    
    serializer_class = EducationalQualificationSerializer 
    queryset = EducationalQualification.objects.all()

    def create(self, request):
        return create_object(EducationalQualificationSerializer, request.data, EducationalQualification)

    def destroy(self, request, pk=None):
        return delete_object(EducationalQualification, pk)

    @action(detail=False, methods=['get'])
    def count(self, request):
        count = get_count(EducationalQualification)
        return Response({"count": count})
    
class LevelViewSet(viewsets.ModelViewSet):
    # permission_classes = [IsAuthenticated]    
    # authentication_classes = [ExpiringTokenAuthentication]     
    queryset = Level.objects.all()
    serializer_class = LevelSerializer

    def create(self,request):
        return create_object(LevelSerializer,request.data,Level)
    
    def destroy(self,request, pk=None):
        return delete_object(Level,pk)
    
    @action (detail=False,methods=['get'])
    def count(self):
        count = get_count(Level)
        return Response({"Count":count})

class SkillViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    authentication_classes = [ExpiringTokenAuthentication] 
    queryset = Skill.objects.all()
    serializer_class = SkillSerializer

    def create(self, request):
        return create_object(SkillSerializer, request.data, Skill)

    def destroy(self, pk=None):
        return delete_object(Skill, pk)

    @action(detail=False, methods=['get'])
    def count(self, request):
        count = get_count(Skill)
        return Response({"Count": count})
  
    
class TeacherSkillViewSet(viewsets.ModelViewSet):
    queryset = TeacherSkill.objects.all()
    permission_classes = [IsAuthenticated]
    authentication_classes = [ExpiringTokenAuthentication] 
    serializer_class = TeacherSkillSerializer
      
    def create(self,request):
        return create_object(TeacherSkillSerializer,request.data,Teacher)
    
    def destroy(self,pk=None):
        return delete_object(TeacherSkill,pk)
    @action(detail=False, methods=['get'])
    def count(self, request):
        count = get_count(TeacherSkill)
        return Response({"Count": count})
    
class SubjectViewSet(viewsets.ModelViewSet):    
    permission_classes = [IsAuthenticated] 
    authentication_classes = [ExpiringTokenAuthentication] 
    queryset = Subject.objects.all()
    serializer_class = SubjectSerializer

    def create(self,request):
        return create_object(SubjectSerializer,request.data,Subject)
    def destory(self,pk=None):
        return delete_object(Subject,pk)
    @action (detail=False,methods=['get'])
    def count(self,request):
        count = get_count(Subject)
        return Response({"Count":count})
    
class TeacherViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    authentication_classes = [ExpiringTokenAuthentication]
    queryset = Teacher.objects.all()
    serializer_class = TeacherSerializer

    @action(detail=False, methods=['get'])
    def count(self, request):
        count = self.get_queryset().count()
        return Response({"count": count})

    def create(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        fullname = serializer.validated_data.get('fullname')
        if Teacher.objects.filter(fullname=fullname).exists():
            return Response(
                {'message': 'Duplicate entry: Teacher already exists.'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        self.perform_create(serializer)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.delete()
        return Response({"message": "Teacher deleted successfully"}, status=status.HTTP_204_NO_CONTENT)

    
    
class ClassCategoryViewSet(viewsets.ModelViewSet):    
    # permission_classes = [IsAuthenticated]
    # authentication_classes = [ExpiringTokenAuthentication] 
    queryset= ClassCategory.objects.all()
    serializer_class = ClassCategorySerializer

    def create(self,request):
        return create_object(ClassCategorySerializer,request.data,ClassCategory)
    def destroy(self,pk=None):
        return delete_object(ClassCategory,pk)
    @action (detail=False,methods=['get'])
    def count(self,request):
        count = get_count(ClassCategory)
        return Response({"Count":count})
    
    
class TeacherQualificationViewSet(viewsets.ModelViewSet): 
    permission_classes = [IsAuthenticated]
    authentication_classes = [ExpiringTokenAuthentication] 
    queryset = TeacherQualification.objects.all()
    serializer_class = TeacherQualificationSerializer

    def create(self,request):
        return create_object(TeacherQualificationSerializer,request.data,TeacherQualification)
    def destroy(self,pk=None):
        return delete_object(TeacherQualification,pk)
    @action (detail=False,methods=['get'])
    def count(self,request):
        count = get_count(TeacherQualification)
        return Response({"count":count})
    
class TeacherExperiencesViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    authentication_classes = [ExpiringTokenAuthentication] 
    queryset = TeacherExperiences.objects.all()
    serializer_class = TeacherExperiencesSerializer

    def create(self,request):
        return create_object(TeacherExperiencesSerializer,request.data,TeacherExperiences)
    def destory(self,pk=None):
        return delete_object(TeacherExperiences,pk)
    @action (detail=False,methods=['get'])
    def count(self,request):
        count = get_count(TeacherExperiences)
        return Response({"Count":count})
    
class QuestionViewSet(viewsets.ModelViewSet):
    queryset = Question.objects.all().select_related('subject', 'level')
    serializer_class = QuestionSerializer
    # permission_classes = [IsAuthenticated]
    # authentication_classes = [ExpiringTokenAuthentication] 

    def create(self,request):
        return create_object(QuestionSerializer,request.data,Question)
    def destory(self,pk=None):
        return delete_object(Question,pk)
    @action (detail=False,methods=['get'])
    def count(self,request):
        count = get_count(Question)
        return Response({"Count":count})