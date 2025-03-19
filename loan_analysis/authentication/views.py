# from django.shortcuts import render, redirect
# from django.contrib.auth import login
# from .form import CustomUserCreationForm  # Import the custom form

# def register(request):
#     if request.method == "POST":
#         form = CustomUserCreationForm(request.POST)
#         if form.is_valid():
#             user = form.save()
#             login(request, user)  # Automatically log in the user after registration
#             return redirect("home")  # Redirect to a home page or dashboard
#     else:
#         form = CustomUserCreationForm()
    
#     return render(request, "authentication/register.html", {"form": form})






# ///////////////////////////////////////////////////////////





from django.shortcuts import render, redirect
from django.contrib.auth import login
from .form import CustomUserCreationForm  # Import the custom form

def register(request):
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  # Automatically log in the user after registration
            return redirect("home")  # Redirect to a home page or dashboard
    else:
        form = CustomUserCreationForm()
    
    return render(request, "authentication/register.html", {"form": form})

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from .forms import BorrowerForm, LenderForm
from .models import BorrowerProfile

@login_required
def apply_loan(request):
    if request.method == "POST":
        form = BorrowerForm(request.POST, request.FILES)
        if form.is_valid():
            borrower = form.save(commit=False)
            borrower.user = request.user
            borrower.status = "Pending"  # Loan is waiting for approval
            borrower.save()
            return redirect('dashboard')
    else:
        form = BorrowerForm()
    return render(request, 'authentication/apply_loan.html', {'form': form})

@login_required
def become_lender(request):
    if request.method == "POST":
        form = LenderForm(request.POST, request.FILES)
        if form.is_valid():
            lender = form.save(commit=False)
            lender.user = request.user
            lender.save()
            return redirect('dashboard')
    else:
        form = LenderForm()
    return render(request, 'authentication/become_lender.html', {'form': form})

@staff_member_required
def approve_loan(request, borrower_id):
    borrower = get_object_or_404(BorrowerProfile, id=borrower_id)
    borrower.status = "Approved"
    borrower.save()
    return redirect('admin-dashboard')

