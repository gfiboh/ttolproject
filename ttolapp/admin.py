from django.contrib import admin
from .models import CustomUser, TeachModel

# Register your models here.
admin.site.register(CustomUser)
admin.site.register(TeachModel)