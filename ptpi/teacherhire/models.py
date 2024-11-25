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

