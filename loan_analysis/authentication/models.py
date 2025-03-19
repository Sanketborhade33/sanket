# from django.contrib.auth.models import AbstractUser, Group, Permission
# from django.db import models

# class CustomUser(AbstractUser):
#     full_name = models.CharField(max_length=255, blank=True, null=True)
#     email = models.EmailField(unique=True)

#     groups = models.ManyToManyField(Group, related_name="customuser_groups", blank=True)
#     user_permissions = models.ManyToManyField(Permission, related_name="customuser_permissions", blank=True)

#     USERNAME_FIELD = "email"
#     REQUIRED_FIELDS = ["username", "full_name"]

#     def __str__(self):
#         return self.email




# ///////////////////////////////



from django.contrib.auth.models import AbstractUser, Group, Permission
from django.db import models

class CustomUser(AbstractUser):
    full_name = models.CharField(max_length=255, blank=True, null=True)
    email = models.EmailField(unique=True)

    groups = models.ManyToManyField(Group, related_name="customuser_groups", blank=True)
    user_permissions = models.ManyToManyField(Permission, related_name="customuser_permissions", blank=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username", "full_name"]

    def __str__(self):
        return self.email

class BorrowerProfile(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    phone = models.CharField(max_length=15)
    address = models.TextField()
    loan_amount = models.DecimalField(max_digits=10, decimal_places=2)
    income_proof = models.FileField(upload_to='documents/')
    credit_score = models.IntegerField()
    loan_purpose = models.TextField()
    status = models.CharField(
        max_length=20, 
        choices=[('Pending', 'Pending'), ('Approved', 'Approved'), ('Rejected', 'Rejected')], 
        default='Pending'
    )

    def __str__(self):
        return f"{self.user.email} - {self.status}"

class LenderProfile(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    phone = models.CharField(max_length=15)
    address = models.TextField()
    investment_amount = models.DecimalField(max_digits=10, decimal_places=2)
    kyc_document = models.FileField(upload_to='documents/')

    def __str__(self):
        return self.user.email

