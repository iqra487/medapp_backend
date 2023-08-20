from django.contrib.auth import login

from rest_framework import generics, permissions
from rest_framework.response import Response
from knox.models import AuthToken

from .models import Appointment, Doctor
from .serializers import AppointmentSerializer, UserSerializer, RegisterSerializer, DoctorSerializer
from knox.views import LoginView as KnoxLoginView
from rest_framework.authtoken.serializers import AuthTokenSerializer

from rest_framework.views import APIView
from rest_framework.exceptions import PermissionDenied




# Register API
class RegisterAPI(generics.GenericAPIView):
    serializer_class = RegisterSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return Response({
        "user": UserSerializer(user, context=self.get_serializer_context()).data,
        "token": AuthToken.objects.create(user)[1]
        })

class LoginAPI(KnoxLoginView):
    permission_classes = (permissions.AllowAny,)

    def post(self, request, format=None):
        serializer = AuthTokenSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        login(request, user)
        return super(LoginAPI, self).post(request, format=None)



class UserProfile(generics.GenericAPIView):
    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request, format=None):
        try:
            doctor = Doctor.objects.get(user_id=request.user.id)
            doctor_serializer = DoctorSerializer(doctor)
            return Response(doctor_serializer.data)
        except Doctor.DoesNotExist:
            user_serializer = UserSerializer(request.user)
            return Response(user_serializer.data)

class DoctorList(generics.ListCreateAPIView):
    queryset = Doctor.objects.all().prefetch_related('hospitals')
    serializer_class = DoctorSerializer

class DoctorDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Doctor.objects.all()
    serializer_class = DoctorSerializer

class AppointmentViewForDoctor(generics.GenericAPIView):
    serializer_class = AppointmentSerializer
    def get(self, request, *args, **kwargs):
        try:
            print('self.request.user.id',request.user)
            doctor = Doctor.objects.get(user_id=request.user.id)
            all_objects =  Appointment.objects.filter(doctor=doctor)
        except Doctor.DoesNotExist:
            all_objects =  Appointment.objects.filter(patient=request.user.id)
        serialize = self.serializer_class(all_objects, many=True)
        return Response(data=serialize.data, status=200)
    
    def post(self, request, *args, **kwargs):
        data = request.data
        try:
            Appointment.objects.create(
                patient_id=request.user.id,
                doctor_id=data['doctor_id'],
                date=data['date'],
                time=data['time']
            )
            return Response(status=201)
        except Exception as e:
            raise Exception("Error while creating appointment", e)