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

class Hospital(models.Model):

    name = models.CharField(max_length=100)
    location = models.EmailField(unique=True, null=True, blank=True)
    lat = models.IntegerField(null=True, blank=True)
    lng = models.IntegerField(null=True, blank=True)
    city = models.CharField(max_length=100, null=True, blank=True)
    state = models.CharField(max_length=100, null=True, blank=True)
    zipcode = models.IntegerField(null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    phone = models.IntegerField(null=True, blank=True)
    email = models.EmailField(unique=True, null=True, blank=True)
    website = models.CharField(max_length=100,null=True, blank=True)

    def __str__(self):
        return self.name


class Doctor(models.Model):

    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    description = models.TextField()
    experience = models.IntegerField()
    choice_field = models.CharField(max_length=20, choices=DOCTOR_TYPE, default='general_physian'),
    hospitals = models.ManyToManyField("Hospital", blank=True)


    user_id= models.OneToOneField(User,on_delete=models.CASCADE)



    def __str__(self):
        return self.name
