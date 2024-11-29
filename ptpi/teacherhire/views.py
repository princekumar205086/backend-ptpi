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

class  RegisterUser(APIView):
    def post(self, request):
        serializers = UserSerializer(data = request.data)

        if not serializers.is_valid():
            return Response({'status': 403, 'error': serializers.errors,'message':'something went worng'})
        
        serializers.save()
        user = User.objects.get(username = serializers.data['username'])
        token_obj , __ = Token.objects.get_or_create(user=user)

        return Response({'status': 200, 'payload': serializers.data,'token':str(token_obj),'message':'your data is save'})
    

def generate_refresh_token():
    refresh_token = str(uuid.uuid4())  
    # refresh_expires_at = datetime.now() + timedelta(minutes=10)  
    return refresh_token

class LoginUser(APIView):
    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')

        user = authenticate(username=username, password=password)
        if user:
            # Delete old token if it exists
            Token.objects.filter(user=user).delete()  
            token = Token.objects.create(user=user) 

            refresh_token = generate_refresh_token()

            return Response({
                'access_token': token.key,   
                'refresh_token': refresh_token,  
                # 'refresh_expires_at': refresh_expires_at,  
                'message': 'Login successful'
            }, status=status.HTTP_200_OK)
        
        return Response({'message': 'Invalid username or password'}, status=status.HTTP_401_UNAUTHORIZED)
            
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
    permission_classes = [IsAuthenticated] 
    authentication_classes = [ExpiringTokenAuthentication]   
    queryset = TeachersAddress.objects.all().select_related('user')
    serializer_class=TeachersAddressSerializer

    @action(detail=False, methods=['get'])
    def count(self, request):
        count = self.get_queryset().count()
        return Response({"count": count})

    
    def create(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        address_type = serializer.validated_data.get('address_type')
        if TeachersAddress.objects.filter(address_type=address_type).exists():
            return Response(
                {'message': 'Duplicate entry: TeachersAddress already exists.'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        self.perform_create(serializer)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.delete()
        return Response({"message": "TeacherAddress deleted successfully"}, status=status.HTTP_204_NO_CONTENT)

#EducationalQulification GET ,CREATE ,DELETE 
class EducationalQulificationViewSet(viewsets.ModelViewSet):    
    permission_classes = [IsAuthenticated] 
    authentication_classes = [ExpiringTokenAuthentication] 
    queryset= EducationalQualification.objects.all()
    serializer_class=EducationalQualificationSerializer

    @action(detail=False, methods=['get'])
    def count(self, request):
        count = self.get_queryset().count()
        return Response({"count": count})

    def create(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        name = serializer.validated_data.get('name')
        if EducationalQualification.objects.filter(name=name).exists():
            return Response(
                {'message': 'Duplicate entry: EducationalQualification already exists.'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        self.perform_create(serializer)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.delete()
        return Response({"message": "EducationalQulification deleted successfully"}, status=status.HTTP_204_NO_CONTENT)



class LevelView(viewsets.ModelViewSet):
    queryset = Level.objects.all()
    serializer_class = LevelSerializer


#Subject GET ,CREATE ,DELETE  
class SkillViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    authentication_classes = [ExpiringTokenAuthentication] 
    queryset = Skill.objects.all()
    serializer_class = SkillSerializer

    @action(detail=False, methods=['get'])
    def count(self, request):
        count = self.get_queryset().count()
        return Response({"count": count})

    def create(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        name = serializer.validated_data.get('name')
        if Skill.objects.filter(name=name).exists():
            return Response(
                {'message': 'Duplicate entry: Skill already exists.'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        self.perform_create(serializer)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.delete()
        return Response({"message": "Skill deleted successfully"}, status=status.HTTP_204_NO_CONTENT)

#Teacher GET ,CREATE ,DELETE 
class TeacherSkillViewSet(viewsets.ModelViewSet):
    queryset = TeacherSkill.objects.all()
    permission_classes = [IsAuthenticated]
    authentication_classes = [ExpiringTokenAuthentication] 
    serializer_class = TeacherSkillSerializer


#Subject GET ,CREATE ,DELETE 

class SubjectViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    authentication_classes = [ExpiringTokenAuthentication] 
    @action(detail=False, methods=['get'])
    def count(self, request):
        count = self.get_queryset().count()
        return Response({"count": count})

    
    def create(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        skill = serializer.validated_data.get('skill')
        if TeacherSkill.objects.filter(skill=skill).exists():
            return Response(
                {'message': 'Duplicate entry: TeacherSkill already exists.'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        self.perform_create(serializer)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.delete()
        return Response({"message": "TeacherSkill deleted successfully"}, status=status.HTTP_204_NO_CONTENT)

class SubjectViewSet(viewsets.ModelViewSet):    
    permission_classes = [IsAuthenticated] 
    authentication_classes = [ExpiringTokenAuthentication] 
    queryset = Subject.objects.all()
    serializer_class = SubjectSerializer

    def create(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        subject_name = serializer.validated_data.get('subject_name')
        if Subject.objects.filter(subject_name=subject_name).exists():
            return Response(
                {'message': 'Duplicate entry: Subject already exists.'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        self.perform_create(serializer)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
    @action(detail=False, methods=['get'])
    def count(self, request):
        count = self.get_queryset().count()
        return Response({"count": count})
    
    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.delete()
        return Response({"message": "Subject deleted successfully"}, status=status.HTTP_204_NO_CONTENT)

#Teacher GET ,DELETE ,POST
class TeacherViewSet(viewsets.ModelViewSet):    
    permission_classes = [IsAuthenticated]
    authentication_classes = [ExpiringTokenAuthentication] 
    queryset= Teacher.objects.all()
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

# Classcategory GET ,DELETE ,POST method
class ClassCategoryViewSet(viewsets.ModelViewSet):    
    permission_classes = [IsAuthenticated]
    authentication_classes = [ExpiringTokenAuthentication] 
    queryset= ClassCategory.objects.all()
    serializer_class = ClassCategorySerializer

    @action(detail=False, methods=['get'])
    def count(self, request):
        count = self.get_queryset().count()
        return Response({"count": count})
    def create(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        name = serializer.validated_data.get('name')
        if ClassCategory.objects.filter(name=name).exists():
            return Response(
                {'message': 'Duplicate entry: ClassCategory already exists.'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        self.perform_create(serializer)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.delete()
        return Response({"message": "ClassCategory deleted successfully"}, status=status.HTTP_204_NO_CONTENT)
    
# TeacherQualification GET ,DELETE ,POST method method
class TeacherQualificationViewSet(viewsets.ModelViewSet): 
    permission_classes = [IsAuthenticated]
    authentication_classes = [ExpiringTokenAuthentication] 
    queryset = TeacherQualification.objects.all()
    serializer_class = TeacherQualificationSerializer

    @action(detail=False, methods=['get'])
    def count(self, request):
        count = self.get_queryset().count()
        return Response({"count": count})

    def create(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        qualification = serializer.validated_data.get('qualification')
        if TeacherQualification.objects.filter(qualification=qualification).exists():
            return Response(
                {'message': 'Duplicate entry: TeacherQualification already exists.'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        self.perform_create(serializer)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.delete()
        return Response({"message": "TeacherQualification deleted successfully"}, status=status.HTTP_204_NO_CONTENT)
      
# TeacherExperiences GET ,DELETE ,POST method method
class TeacherExperiencesViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    authentication_classes = [ExpiringTokenAuthentication] 
    queryset = TeacherExperiences.objects.all()
    serializer_class = TeacherExperiencesSerializer

    @action(detail=False, methods=['get'])
    def count(self, request):
        count = self.get_queryset().count()
        return Response({"count": count})
    def create(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        institution = serializer.validated_data.get('institution')
        if TeacherExperiences.objects.filter(institution=institution).exists():
            return Response(
                {'message': 'Duplicate entry: TeacherExperiences already exists.'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        self.perform_create(serializer)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.delete()
        return Response({"message": "TeacherExperiences deleted successfully"}, status=status.HTTP_204_NO_CONTENT)
    
class QuestionViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication] 
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer

    @action(detail=False, methods=['get'])
    def count(self, request):
        count = self.get_queryset().count()
        return Response({"count": count})
    
    def create(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        institution = serializer.validated_data.get('institution')
        if Question.objects.filter(institution=institution).exists():
            return Response(
                {'message': 'Duplicate entry: TeacherExperiences already exists.'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        self.perform_create(serializer)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.delete()
        return Response({"message": "Question deleted successfully"}, status=status.HTTP_204_NO_CONTENT)
      
