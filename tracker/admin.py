from django.contrib import admin
from .models import Workout

# Register your models here.
admin.site.register(Workout) # Tells Django to include the Workout model in the admin interface
