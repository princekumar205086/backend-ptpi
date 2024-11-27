from django.db import models
from django.contrib.auth.models import User

# Create your models here.   
class TeachersAddress(models.Model):
    ADDRESS_TYPE_CHOICES = [
        ('current', 'Current'),
        ('permanent', 'Permanent'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    address_type = models.CharField(max_length=10, choices=ADDRESS_TYPE_CHOICES)
    state = models.CharField(max_length=100, default='Bihar')
    division = models.CharField(max_length=100)
    district = models.CharField(max_length=100)
    block = models.CharField(max_length=100)
    village = models.CharField(max_length=100)
    area = models.TextField(null=True, blank=True)
    pincode = models.CharField(max_length=6)

    def __str__(self):
        return f'{self.address_type} address of {self.user.username}'

# Create your models here.
class Subject(models.Model):
    subject_name = models.CharField(max_length=100)
    subject_description = models.TextField(null=True, blank=True)
    def __str__(self):
        return self.subject_name

class ClassCategory(models.Model):
    name = models.CharField(
        max_length=100,
        unique=True,
        choices=[
            ("Nursery to U.K.G","Nursery to U.K.G"),
            ("1 to 5","1 to 5"),
            ("6 to 8","6 to 8"),
            ("9 to 10","9 to 10"),
            ("10 to 12","10 to 12")
        ]
        )
    def __str__(self):
        return self.name
class Teacher(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    fullname = models.	CharField(max_length=255)
    gender	 = models.CharField(
        max_length=10,
        choices=[
            ("Female","Female"),
            ("Male","Male"),
            ("other","other"),
        ])
    religion = models.	CharField(max_length=100)
    nationality = models. CharField(
        max_length=100,
        choices=[
            ("Indian","Indian"),
            ("other","other"),
        ]
        )
    image = models.	ImageField(upload_to='images/',null=True)
    aadhar_no = models.CharField(max_length=12, unique=True)
    phone = models.	CharField(max_length=15)
    alternate_phone = models. CharField(max_length=15, null=True, blank=True)
    verified = models.	BooleanField(default=False)
    class_categories = models.ForeignKey(ClassCategory, on_delete=models.CASCADE)
    rating = models. DecimalField(max_digits=3, decimal_places=2, null=True, blank=True)
    date_of_birth = models.	DateField()
    availability_status = models.CharField(max_length=50, default='Available')
    def __str__(self):
        return self.user

class EducationalQualification(models.Model):	
   name = models.CharField(max_length=255, unique=True)
   description = models.TextField(null=True, blank=True)

   def _str_(self):
        return self.name

class TeacherQualification(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    qualification = models.ForeignKey(EducationalQualification, on_delete=models.CASCADE)
    institution = models.CharField(max_length=225)  
    year_of_passing = models.PositiveIntegerField()  
    grade_or_percentage = models.CharField(max_length=50, null=True, blank=True)

    def _str_(self):
        return self.user

class TeacherExperiences(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    institution = models.CharField(max_length=255)
    role = models.CharField(max_length=255)
    start_date	= models.DateField()
    end_date = models.DateField(null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    achievements = models.TextField(null=True, blank=True)

    def _str_(self):
        return self.user

class Skill(models.Model):
   name = models.CharField(max_length=255, unique=True)
   description = models.TextField(null=True, blank=True)

   def _str_(self):
        return self.name

class TeacherSkill(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    skill = models.ForeignKey(Skill, on_delete=models.CASCADE)
    proficiency_level = models.CharField(max_length=100, null=True, blank=True)
    years_of_experience = models.PositiveIntegerField(default=0)
    
    def _str_(self):
        return self.user


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")
    bio = models.TextField(blank=True, null=True)
    profile_picture = models.ImageField(upload_to='profile_pics/', blank=True, null=True)
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    is_teacher = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Profile of {self.user.username}"