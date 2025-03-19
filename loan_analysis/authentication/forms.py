from django import forms
from .models import BorrowerProfile, LenderProfile

class BorrowerForm(forms.ModelForm):
    class Meta:
        model = BorrowerProfile
        fields = ['phone', 'address', 'loan_amount', 'income_proof', 'credit_score', 'loan_purpose']

class LenderForm(forms.ModelForm):
    class Meta:
        model = LenderProfile
        fields = ['phone', 'address', 'investment_amount', 'kyc_document']
