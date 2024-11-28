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
            serializer = LoginSerializer(data = request.data)
            if serializer.is_valid(raise_exception=True):
                user = authenticate(username=serializer.data['username'], password=serializer.data['password'])
                if user:
                    token, created = Token.objects.get_or_create(user=user)
                    return Response({'token': [token.key], "Sucsses":"Login SucssesFully"}, status=status.HTTP_201_CREATED )
                return Response({'Massage': 'Invalid Username and Password'}, status=401)

    
class UserProfileViewSet(viewsets.ModelViewSet):
    #permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]   
    queryset = UserProfile.objects.all().select_related('user')
    serializer_class = UserProfileSerializer

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.delete()
        return Response({"message": "UserProfile deleted successfully"}, status=status.HTTP_204_NO_CONTENT)

#TeacerAddress GET ,CREATE ,DELETE 
class TeachersAddressViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated] 
    authentication_classes = [TokenAuthentication]   
    queryset = TeachersAddress.objects.all().select_related('user')
    serializer_class=TeachersAddressSerializer

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.delete()
        return Response({"message": "TeacherAddress deleted successfully"}, status=status.HTTP_204_NO_CONTENT)

#EducationalQulification GET ,CREATE ,DELETE 
class EducationalQulificationViewSet(viewsets.ModelViewSet):    
    permission_classes = [IsAuthenticated] 
    authentication_classes = [TokenAuthentication] 
    queryset= EducationalQualification.objects.all()
    serializer_class=EducationalQualificationSerializer

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.delete()
        return Response({"message": "EducationalQulification deleted successfully"}, status=status.HTTP_204_NO_CONTENT)

#Subject GET ,CREATE ,DELETE  
class SkillViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication] 
    queryset = Skill.objects.all()
    serializer_class = SkillSerializer

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.delete()
        return Response({"message": "Skill deleted successfully"}, status=status.HTTP_204_NO_CONTENT)

#Teacher GET ,CREATE ,DELETE 
class TeacherSkillViewSet(viewsets.ModelViewSet):
    queryset = TeacherSkill.objects.all()
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication] 
    serializer_class = TeacherSkillSerializer

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.delete()
        return Response({"message": "TeacherSkill deleted successfully"}, status=status.HTTP_204_NO_CONTENT)

#Subject GET ,CREATE ,DELETE 
class SubjectViewSet(viewsets.ModelViewSet):    
    permission_classes = [IsAuthenticated] 
    authentication_classes = [TokenAuthentication] 
    queryset= Subject.objects.all()
    serializer_class = SubjectSerializer

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.delete()
        return Response({"message": "Subject deleted successfully"}, status=status.HTTP_204_NO_CONTENT)




#Teacher GET ,DELETE ,POST
class TeacherViewSet(viewsets.ModelViewSet):    
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication] 
    queryset= Teacher.objects.all()
    serializer_class = TeacherSerializer

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.delete()
        return Response({"message": "Teacher deleted successfully"}, status=status.HTTP_204_NO_CONTENT)

# Classcategory GET ,DELETE ,POST method
class ClassCategoryViewSet(viewsets.ModelViewSet):    
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication] 
    queryset= ClassCategory.objects.all()
    serializer_class = ClassCategorySerializer

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.delete()
        return Response({"message": "ClassCategory deleted successfully"}, status=status.HTTP_204_NO_CONTENT)
    
# TeacherQualification GET ,DELETE ,POST method method
class TeacherQualificationViewSet(viewsets.ModelViewSet): 
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication] 
    queryset = TeacherQualification.objects.all()
    serializer_class = TeacherQualificationSerializer

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.delete()
        return Response({"message": "TeacherQualification deleted successfully"}, status=status.HTTP_204_NO_CONTENT)
      
# TeacherExperiences GET ,DELETE ,POST method method
class TeacherExperiencesViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication] 
    queryset = TeacherExperiences.objects.all()
    serializer_class = TeacherExperiencesSerializer

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.delete()
        return Response({"message": "TeacherExperiences deleted successfully"}, status=status.HTTP_204_NO_CONTENT)
      
