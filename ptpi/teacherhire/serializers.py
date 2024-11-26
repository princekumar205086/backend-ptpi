from rest_framework import serializers
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from teacherhire.models import TeacherQualification, TeacherExperiences

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'password']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User.objects.create(
            username=validated_data['username'],
            email=validated_data['email'],
        )
        user.set_password(validated_data['password'])
        user.save()
        return user

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(style={'input_type': 'password'}, write_only=True)

    class Meta:
        model = User
        fields = ['email', 'username', 'password']

    def validate_email(self, value):
        if ' ' in value:
            raise serializers.ValidationError("Email cannot contain spaces.")
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError("A user with this email already exists.")
        return value
    def validate(self, attrs):        
        password = attrs.get('password')        
        if ' ' in password:
            raise serializers.ValidationError("Password cannot contain spaces.")
    
        return attrs  
    def create(self, validated_data):
        user = User.objects.create(
            username=validated_data['username'],
            email=validated_data['email'],
        )
        user.set_password(validated_data['password'])
        user.save()
        return user

class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(style={'input_type': 'password'}, write_only=True)

    def validate(self, data):
        email = data.get('email')
        password = data.get('password')

        user = authenticate(username=email, password=password)
        
        if not user:
            raise serializers.ValidationError("Invalid email or password, please try again.")
        
        data['user'] = user
        return data
    
   

# Create your views here.

class TeacherQualificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = TeacherQualification
        fields = "_all_"

class TeacherExperiencesSerializer(serializers.ModelSerializer):
    class Meta:
        model = TeacherExperiences
        fields = "_all_"



