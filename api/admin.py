from django.contrib import admin

from api.models import Doctor
from api.models import Hospital

# Register your models here.
admin.site.register(Doctor)
admin.site.register(Hospital)