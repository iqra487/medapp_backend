from django.db import models

# Create your models here.
from django.db import models
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.http import JsonResponse
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import User
from django.contrib.postgres.fields import ArrayField



class UserRegistration(models.Model):
    username = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=100)
    registration_token = models.CharField(max_length=255)


DOCTOR_TYPE = [
    ('general_physicipyton an', 'General Physician'),
    ('Specialist', 'Specialist'),
    ('Surgeon', 'Surgeon'),
    # Add more choices as needed
]
class Doctor(models.Model):

    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    description = models.TextField()
    experience = models.IntegerField()
    choice_field = models.CharField(max_length=20, choices=DOCTOR_TYPE, default='general_physian'),
    hospitals = models.CharField(max_length=200, default='Pet Hospital')


    user_id= models.OneToOneField(User,on_delete=models.CASCADE)



    def __str__(self):
        return self.name

