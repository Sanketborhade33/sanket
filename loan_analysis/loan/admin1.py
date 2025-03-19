from django.contrib import admin1
from .models import LoanApplication

# Register the model
@admin1.register(LoanApplication)
class LoanApplicationAdmin(admin1.ModelAdmin):
    list_display = ("name", "email", "amount", "purpose", "created_at")  # Customize displayed columns
    search_fields = ("name", "email")  # Add search functionality
    list_filter = ("amount", "created_at")  # Add filters

# OR (Alternative registration method)
# admin.site.register(LoanApplication)
