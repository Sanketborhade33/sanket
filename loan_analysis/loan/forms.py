


from django import forms
from .models import Lender

# class LenderForm(forms.ModelForm):
#     class Meta:
#         model = Lender
#         fields = ['name', 'email', 'phone', 'company_name', 'loan_amount', ]


from .models import Lender

class LenderForm(forms.ModelForm):
    class Meta:
        model = Lender
        fields = ['name', 'company_name', 'email', 'phone', 'loan_amount', 'interest_rate', 'lending_period']



from django import forms
from .models import Borrower

class BorrowerForm(forms.ModelForm):
    class Meta:
        model = Borrower
        fields = ['name', 'email', 'phone', 'loan_amount', 'purpose']

