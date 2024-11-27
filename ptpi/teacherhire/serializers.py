from django.contrib.auth.models import User
from .models import TeachersAddress,EducationalQualification
from django.contrib.auth import authenticate
from rest_framework import serializers
from teacherhire.models import Subject,UserProfile,Teacher,ClassCategory, Skill, TeacherSkill, TeacherQualification, TeacherExperiences


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
import re
from rest_framework import serializers
from django.contrib.auth.models import User
from .models import UserProfile

class UserProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    profile_picture = serializers.ImageField(required=False, allow_null=True)

    class Meta:
        model = UserProfile
        fields = ['user', 'bio', 'profile_picture', 'phone_number', 'address', 'is_teacher', 'created_at', 'updated_at']

    def create(self, validated_data):        
        return UserProfile.objects.create(**validated_data)

    def update(self, instance, validated_data): 
        for field, value in validated_data.items():
            setattr(instance, field, value)        
        instance.save()
        return instance

    def validate_bio(self, value):
        
        value = value.strip() if value else ""
        if not value:
            raise serializers.ValidationError("Bio cannot be empty or just spaces.")
        return value

    def validate_address(self, value):        
        value = value.strip() if value else ""
        if not value:
            raise serializers.ValidationError("Address cannot be empty or just spaces.")
        return value

    def validate_phone_number(self, value):       
        if value:
            cleaned_value = re.sub(r'[^0-9]', '', value)
            if len(cleaned_value) < 10:
                raise serializers.ValidationError("Phone number must have at least 10 digits.")
            
            return cleaned_value
        
        return value

    def validate_profile_picture(self, value):        
        if value and value.size > 5 * 1024 * 1024: 
            raise serializers.ValidationError("Profile picture must be under 5 MB.")
        return value

    def validate(self, data):
    
        if 'phone_number' in data and len(data['phone_number']) < 10:
            raise serializers.ValidationError({"phone_number": "Phone number must have at least 10 digits."})
        return data

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
    
   

# def validate_blank_fields(data):
#     for field, value in data.items():
#         if isinstance(value, str) and value.strip() == '':
#             raise serializers.ValidationError(f"{field} cannot be empty or just spaces.")
#     return data

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
        fields = ['user_id', 'skill', 'proficiency_level', ]
        
class TeachersAddressSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())
    class Meta:
        model = TeachersAddress
        fields = '__all__'
        
    def validate_user(self,value):
        try:
            user = User.objects.get(id=value.id)
        except User.DoesNotExist:
            raise serializers.ValidationError("The user does not exist.")        
        return value
    # def validate(self, data):
    #     return validate_blank_fields(data)
    
class EducationalQualificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = EducationalQualification
        fields = '__all__'
