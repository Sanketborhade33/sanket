# from django.contrib import admin

# Register your models here.

from django.contrib import admin
from .models import Lender

admin.site.register(Lender)



from .models import Borrower

admin.site.register(Borrower)
