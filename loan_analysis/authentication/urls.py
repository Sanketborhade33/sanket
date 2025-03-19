# from django.urls import path
# from authentication.views import register
# from django.contrib.auth import views as auth_views

# urlpatterns = [
#     path("register/", register, name="register"),
#     path("login/", auth_views.LoginView.as_view(template_name="authentication/login.html"), name="login"),
#     path("logout/", auth_views.LogoutView.as_view(), name="logout"),
# ]





# ///////////////////////////////////////////////////////



from django.urls import path
from authentication.views import register
from django.contrib.auth import views as auth_views
from .views import apply_loan, become_lender, approve_loan

urlpatterns = [
    path("register/", register, name="register"),
    path("login/", auth_views.LoginView.as_view(template_name="authentication/login.html"), name="login"),
    path("logout/", auth_views.LogoutView.as_view(), name="logout"),
    path('apply-loan/', apply_loan, name='apply-loan'),
    path('become-lender/', become_lender, name='become-lender'),
    path('approve-loan/<int:borrower_id>/', approve_loan, name='approve-loan'),
]