from django.contrib import admin
from .models import *
from .models import Camera
# Register your models here.
admin.site.register(MissingPerson)
admin.site.register(Location)
admin.site.register(Camera)