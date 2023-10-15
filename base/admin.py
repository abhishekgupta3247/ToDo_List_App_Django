from django.contrib import admin

# Register your models here.

# Registering our model (Task) with admin panel
 
from .models import Task

admin.site.register(Task)