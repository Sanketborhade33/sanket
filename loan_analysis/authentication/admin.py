from django.contrib import admin
from authentication.models import CustomUser  # Import your CustomUser model

admin.site.register(CustomUser)  # Register CustomUser in the admin panel
