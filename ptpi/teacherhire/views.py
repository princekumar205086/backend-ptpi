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
    

class LoginUser(APIView):
    serializer_class = LoginSerializer

    authentication_classes = [TokenAuthentication]
 
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            user = authenticate(username=serializer.data['username'], password=serializer.data['password'])
            if user:
                token, created = Token.objects.get_or_create(user=user)
                
                refresh_token = str(uuid.uuid4())  
                                
                return Response({
                    'token': token.key,
                    'refresh_token': refresh_token,  
                    "success": "Login Successfully"
                }, status=status.HTTP_201_CREATED)
                
            return Response({'message': 'Invalid Username or Password'}, status=status.HTTP_401_UNAUTHORIZED)
            
class LogoutUser(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            token = Token.objects.get(user=request.user)
            token.delete()
            return Response({"success": "Logout successful"}, status=status.HTTP_200_OK)
        except Token.DoesNotExist:
            return Response({"error": "Invalid or expired token"}, status=status.HTTP_400_BAD_REQUEST)

    
class UserProfileViewSet(viewsets.ModelViewSet):
    #permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]   
    queryset = UserProfile.objects.all().select_related('user')
    serializer_class = UserProfileSerializer

#TeacerAddress GET ,CREATE ,DELETE 
class TeachersAddressViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated] 
    authentication_classes = [TokenAuthentication]   
    queryset = TeachersAddress.objects.all().select_related('user')
    serializer_class=TeachersAddressSerializer

#EducationalQulification GET ,CREATE ,DELETE 
class EducationalQulificationViewSet(viewsets.ModelViewSet):    
    permission_classes = [IsAuthenticated] 
    authentication_classes = [TokenAuthentication] 
    queryset= EducationalQualification.objects.all()
    serializer_class=EducationalQualificationSerializer

#Subject GET ,CREATE ,DELETE  
class SkillViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication] 
    queryset = Skill.objects.all()
    serializer_class = SkillSerializer

#Teacher GET ,CREATE ,DELETE 
class TeacherSkillViewSet(viewsets.ModelViewSet):
    queryset = TeacherSkill.objects.all()
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication] 
    serializer_class = TeacherSkillSerializer

#Subject GET ,CREATE ,DELETE 
class SubjectViewSet(viewsets.ModelViewSet):    
    permission_classes = [IsAuthenticated] 
    authentication_classes = [TokenAuthentication] 
    queryset= Subject.objects.all()
    serializer_class = SubjectSerializer

#Teacher GET ,DELETE ,POST
class TeacherViewSet(viewsets.ModelViewSet):    
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication] 
    queryset= Teacher.objects.all()
    serializer_class = TeacherSerializer

# Classcategory GET ,DELETE ,POST method
class ClassCategoryViewSet(viewsets.ModelViewSet):    
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication] 
    queryset= ClassCategory.objects.all()
    serializer_class = ClassCategorySerializer
    
# TeacherQualification GET ,DELETE ,POST method method
class TeacherQualificationViewSet(viewsets.ModelViewSet): 
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication] 
    queryset = TeacherQualification.objects.all()
    serializer_class = TeacherQualificationSerializer
      
# TeacherExperiences GET ,DELETE ,POST method method
class TeacherExperiencesViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication] 
    queryset = TeacherExperiences.objects.all()
    serializer_class = TeacherExperiencesSerializer
      
