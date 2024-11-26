from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from rest_framework import serializers
from teacherhire.models import Subject,Teacher,ClassCategory, Skill, TeacherSkill, TeacherQualification, TeacherExperiences


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
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError("A user with this email already exists.")
        return value

    def create(self, validated_data):
        user = User.objects.create(
            username=validated_data['username'],
            email=validated_data['email'],
        )
        user.set_password(validated_data['password'])
        user.save()
        return user

# Login Serializer (for User Login)
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
class SubjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subject
        fields = ['subject_name','subject_description']

class ClassCategorySerializer(serializers.ModelSerializer):
    # user = UserSerializer(read_only=True) 
    class Meta:
        model =ClassCategory
        fields = ['name']

class TeacherSerializer(serializers.ModelSerializer):
    # user = UserSerializer(read_only=True) 
    class Meta:
        model = Teacher
        fields = "__all__"

class SkillSerializer(serializers.ModelSerializer):
    class Meta:
        model = Skill
        fields = "__all__"

class TeacherSkillSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(queryset=User.objects.all(), required=True)
    skill = serializers.PrimaryKeyRelatedField(queryset=Skill.objects.all(), required=True)

    class Meta:
        model = TeacherSkill
        fields = ['id', 'user', 'skill', 'proficiency_level']  

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['user'] = UserSerializer(instance.user).data
        representation['skill'] = SkillSerializer(instance.skill).data
        return representation
