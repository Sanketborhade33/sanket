from django.db import models
from django.conf import settings  # Import settings to get AUTH_USER_MODEL

# Loan Application Model
# class LoanApplication(models.Model):
#     name = models.CharField(max_length=100)
#     employment_status = models.CharField(max_length=50)
#     monthly_income = models.FloatField()
#     existing_loans = models.IntegerField()
#     credit_score = models.FloatField()
#     loan_amount_requested = models.FloatField()
#     debt_to_income_ratio = models.FloatField()
#     loan_purpose = models.CharField(max_length=100)
#     repayment_history = models.CharField(max_length=50)
#     defaulted = models.BooleanField()  # Target variable (Yes/No)

#     def __str__(self):
#         return f"{self.name} - {self.loan_purpose} (Defaulted: {'Yes' if self.defaulted else 'No'})"



class LoanApplication(models.Model):
    name = models.CharField(max_length=255)
    email = models.EmailField()  # Ensure this field exists
    amount = models.DecimalField(max_digits=10, decimal_places=2, default=1000)  # Default value set
    purpose = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} - {self.amount}"

# Lender Model
# class Lender(models.Model):
#     name = models.CharField(max_length=255)
#     email = models.EmailField(unique=True)
#     phone = models.CharField(max_length=15)
#     company_name = models.CharField(max_length=255, blank=True, null=True)
#     loan_amount = models.DecimalField(max_digits=10, decimal_places=2)
#     created_at = models.DateTimeField(auto_now_add=True)
    
#     def __str__(self):
#         return self.name




from django.db import models

class Lender(models.Model):
    name = models.CharField(max_length=255)
    company_name = models.CharField(max_length=255, blank=True, null=True)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=15)
    loan_amount = models.DecimalField(max_digits=10, decimal_places=2)  # Amount willing to lend
    interest_rate = models.DecimalField(max_digits=5, decimal_places=2, default=5.0)
    lending_period = models.IntegerField(help_text="Lending Period (months)")
    available_balance = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)  # Remaining lending balance
    is_active = models.BooleanField(default=True)  # Active lender

    def __str__(self):
        return f"{self.name} - {self.company_name if self.company_name else 'Individual'}"












# Borrower Model
class Borrower(models.Model):
    name = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=15)
    loan_amount = models.DecimalField(max_digits=10, decimal_places=2)
    purpose = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

# Chat Message Model
class ChatMessage(models.Model):
    sender = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="sent_messages")
    receiver = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="received_messages")
    message = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['timestamp']  # Ensures messages are retrieved in chronological order

    def __str__(self):
        return f"Message from {self.sender} to {self.receiver} at {self.timestamp}"
