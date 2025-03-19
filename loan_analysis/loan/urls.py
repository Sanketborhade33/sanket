from django.urls import path
from .views import (
    home, 
    user_login, 
    lender_list, 
    borrower_list, 
    lender_registration, 
    borrower_registration, 
    chat_room
)

urlpatterns = [
    path("", home, name="home"),
    path("login/", user_login, name="login"),
    path("register/", lender_registration, name="lender_registration"),
    path("lenders/", lender_list, name="lender_list"),
    path("borrower/register/", borrower_registration, name="borrower_registration"),
    path("borrowers/", borrower_list, name="borrower_list"),  # Only one definition
    path("chat/<int:receiver_id>/", chat_room, name="chat_room"),
]







