from rest_framework import serializers
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token
from rest_framework.relations import PrimaryKeyRelatedField
from api.models import Hospital
from api.models import Doctor


# User Serializer
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email')


# Register Serializer
class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'password')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User.objects.create_user(validated_data['username'], validated_data['email'], validated_data['password'])

        return user

class HospitalSerializer(serializers.ModelSerializer):
    class Meta:
        model = Hospital
        fields = ['id', 'name', 'location', 'lat', 'lng', 'city', 'state', 'zipcode', 'description', 'phone', 'email', 'website']

class HospitalSerializerMini(serializers.ModelSerializer):
    class Meta:
        model = Hospital
        fields = ['id', 'name', 'location']

class DoctorSerializer(serializers.ModelSerializer):
    hospitals =  HospitalSerializerMini(many=True, read_only=True)
    class Meta:
        model = Doctor
        fields = ['id', 'name', 'email', 'description', 'experience', 'user_id', 'hospitals']

