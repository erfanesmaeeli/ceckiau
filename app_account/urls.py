from django.urls import path
from app_account import views

urlpatterns = [
    path('signup/', views.signup , name = "signup"),
    path('profile/', views.profile , name = "profile"),
    path('reset-password/', views.reset_password , name = "reset-password"),
    path('staff-signup/', views.staff_signup , name = "staff-signup"),
]