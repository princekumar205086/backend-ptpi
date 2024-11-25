from django.db import models

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
    user_id = models.ForeignKey(User,on_delete=models.CASCADE)
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
    image = models.	ImageField(upload_to='images/')
    aadhar_no = models.CharField(max_length=12, unique=True)
    phone = models.	CharField(max_length=15)
    alternate_phone = models. CharField(max_length=15, null=True, blank=True)
    verified = models.	BooleanField(default=False)
    class_categories = models.ForeignKey(ClassCategory, on_delete=models.CASCADE)
    rating = models. DecimalField(max_digits=3, decimal_places=2, null=True, blank=True)
    date_of_birth = models.	DateField()
    availability_status = models.CharField(max_length=50, default='Available')
    def __str__(self):
        return self.user_id