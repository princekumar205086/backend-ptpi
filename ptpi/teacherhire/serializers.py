from django.contrib.auth.models import User
from .models import TeachersAddress,EducationalQualification
from django.contrib.auth import authenticate
from rest_framework import serializers
import re
from teacherhire.models import Subject,UserProfile,Teacher,ClassCategory, Skill, TeacherSkill, TeacherQualification, TeacherExperiences
from teacherhire.models import *
import re
from datetime import date
import random
from .models import UserProfile
from django.contrib.auth.models import User
from rest_framework.exceptions import ValidationError


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'password']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
         user = User.objects.create(
            username=validated_data['username'],
            # email=validated_data['email'],
        )
         user.set_password(validated_data['password'])
         user.save()
         return user
    


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ['email', 'password']

    def create(self, validated_data):
        email = validated_data['email']
        base_username = email.split('@')[0] 
        username = base_username
        if User.objects.filter(email=email).exists():
            raise ValidationError({'email': 'Email is already in use.'})
        while User.objects.filter(username=username).exists():
            username = f"{base_username}{random.randint(1000, 9999)}"  
        try:
            user = User.objects.create_user(
                username=username,
                email=email,
                password=validated_data['password']
            )
        except Exception as e:
            raise ValidationError({'error': str(e)})
        return user
    
class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField(max_length=100)
    password = serializers.CharField(max_length=100)

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

class TeacherExperiencesSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(queryset=User.objects.all(), required=True)
    institution = serializers.CharField(max_length=255, required=False, allow_null=True)
    role = serializers.CharField(max_length=255, required=False, allow_null=True)
    start_date = serializers.DateField(required=False, allow_null=True)
    end_date = serializers.DateField(required=False, allow_null=True)
    achievements = serializers.CharField(required=False, allow_null=True)

    class Meta:
        model = TeacherExperiences
        fields = "__all__"
        
    def validate_institution(self, value):
        if value and len(value) < 3:
            raise serializers.ValidationError("Institution name must be at least 3 characters long.")
        return value
    
    def validate(self, data):
        start_date = data.get('start_date')
        end_date = data.get('end_date')

        if start_date and end_date:
            if start_date > end_date:
                raise serializers.ValidationError("End date cannot be earlier than start date.")
        
        return data
    def validate_achievements(self, value):        
        if value:
            value = value.strip()
            if len(value) < 10:
                raise serializers.ValidationError("Achievements must be at least 10 characters long.")
        return value
    def to_representation(self, instance):
        representation = super().to_representation(instance)
        if instance.user:
            representation['user'] = UserSerializer(instance.user).data
        return representation
    
class SubjectSerializer(serializers.ModelSerializer):
    # subject_name = serializers.CharField(max_length=255, requirement=False, allow_null=True)
    class Meta:
        model = Subject
        fields = ['id','subject_name','subject_description']
    # def validate_subject_name(value):
    #     if len(value) < 2 or len(value) > 10:
    #         raise serializers.ValidationError("Subject name must be between 2 and 10 characters long.")
    #     return value
class ClassCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = ClassCategory
        fields = ['id','name']

class LevelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Level
        fields = '__all__'
class TeachersAddressSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(queryset=User.objects.all(), required=True)
    pincode = serializers.CharField(max_length=6, required=False, allow_null=True)

    class Meta:
        model = TeachersAddress
        fields = '__all__'

    def validate_pincode(self, value):
        if value and (len(value) != 6 or not value.isdigit()):
            raise serializers.ValidationError("Pincode must be exactly 6 digits.")
        return value

# TeacherSerializer
class TeacherSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(queryset=User.objects.all(), required=True)
    # teachers_address = TeachersAddressSerializer(many=False, allow_null=True)
    aadhar_no = serializers.CharField(max_length=12, required=False, allow_null=True)
    fullname = serializers.CharField(max_length=20, required=False, allow_null=True)
    phone = serializers.CharField(max_length=10, required=False, allow_null=True)
    alternate_phone = serializers.CharField(max_length=10, required=False, allow_null=True)
    date_of_birth = serializers.DateField(required=False, allow_null=True)

    address = serializers.SerializerMethodField()  

    class Meta:
        model = Teacher
        fields = [
            'id', 'user', 'fullname', 'gender', 'religion', 'nationality',
            'aadhar_no', 'phone', 'alternate_phone', 'verified',
            'class_categories', 'rating', 'date_of_birth',
            'availability_status', 'address'
        ]

    def validate_fullname(self, value): 
        if value is not None:
            value = value.strip()
            if len(value) < 3:
                raise serializers.ValidationError("Full name must be at least 3 characters.")
        return value

    def validate_phone(self, value):       
        return self.validate_phone_number(value)

    def validate_alternate_phone(self, value):        
        return self.validate_phone_number(value)

    def validate_phone_number(self, value):
        if value:
            cleaned_value = re.sub(r'[^0-9]', '', value)  # Removing non-digit characters
            if len(cleaned_value) != 10:
                raise serializers.ValidationError("Phone number must be exactly 10 digits.")
            if not cleaned_value.startswith(('6', '7', '8', '9')):
                raise serializers.ValidationError("Phone number must start with 6, 7, 8, or 9.")
            return cleaned_value
        return value

    def validate_aadhar_no(self, value):        
        if value:
            if not re.match(r'^\d{12}$', value):
                raise serializers.ValidationError("Aadhar number must be exactly 12 digits.")
        return value
    
    
    def to_representation(self, instance):    
        representation = super().to_representation(instance)
        representation['user'] = UserSerializer(instance.user).data
        return representation
    
    def get_address(self, obj):
        addresses = TeachersAddress.objects.filter(user=obj.user)
        return TeachersAddressSerializer(addresses, many=True).data  
    
    

    
    
class SkillSerializer(serializers.ModelSerializer):
    name = serializers.CharField(max_length=20, required=False, allow_null=True)
    class Meta:
        model = Skill
        fields = "__all__"
    def validate_name(self,value):
        if value is not None:
            if len(value) < 3:
                raise serializers.ValidationError("Skill name must be at least 3 characters.")
        return value
    
class QuestionSerializer(serializers.ModelSerializer):
    subject = serializers.PrimaryKeyRelatedField(queryset=Subject.objects.all(), required=True)
    level = serializers.PrimaryKeyRelatedField(queryset=Level.objects.all(), required=True)
    text = serializers.CharField(max_length=2000,allow_null=True, required=False)
    options = serializers.JSONField(required=False, allow_null=True)    
    correct_options = serializers.ListField(
        child=serializers.IntegerField(min_value=0), 
        required=False,
        allow_null=True
    )  
    class Meta:
        model = Question
        fields = "__all__"
    def validate_text(self,value):
        if value is not None:
            if len(value) < 5:
                raise serializers.ValidationError("Text must be at least 5 characters.")
            return value
    def validate_options(self, value):
        if value is not None:
            if not isinstance(value, list):
                raise serializers.ValidationError("Options must be a list.")
            if len(value) != 4:
                raise serializers.ValidationError("Options must contain exactly 4 items.")
        return value
    def validate_correct_options(self, value):
        if value is not None:
            if not isinstance(value, list):
                raise serializers.ValidationError("Correct options must be a list of indices.")
            if len(value) == 0:
                raise serializers.ValidationError("At least one correct option must be specified.")
            if any(option >= len(self.initial_data.get('options', [])) for option in value):
                raise serializers.ValidationError("Correct options must be valid indices of the options list.")
            if len(value) != len(set(value)):
                raise serializers.ValidationError("Correct options must contain unique indices.")
        return value
    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['subject'] = SubjectSerializer(instance.subject).data
        representation['level'] = LevelSerializer(instance.level).data
        return representation
        
class TeacherSkillSerializer(serializers.ModelSerializer):
    
    user = serializers.PrimaryKeyRelatedField(queryset=User.objects.all(), required=True)
    skill = serializers.PrimaryKeyRelatedField(queryset=Skill.objects.all(), required=False)

    class Meta:
        model = TeacherSkill
        fields = ['id', 'user', 'skill', 'proficiency_level']  

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['user'] = UserSerializer(instance.user).data
        representation['skill'] = SkillSerializer(instance.skill).data
        return representation
            
class EducationalQualificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = EducationalQualification
        fields = '__all__'
class TeacherQualificationSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(queryset=User.objects.all(),required=True)
    qualification = serializers.PrimaryKeyRelatedField(queryset=EducationalQualification.objects.all(),required=True)
    class Meta:
        model = TeacherQualification
        fields = "__all__"
    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['user'] = UserSerializer(instance.user).data
        representation['qualification'] = EducationalQualificationSerializer(instance.qualification).data
        return representation

