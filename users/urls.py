from django.urls import path
from .views import LoginView, log_out, SignupView, complete_verification

app_name = "users"

urlpatterns = [
    path("login/", LoginView.as_view(), name="login"),
    path("logout/", log_out, name="logout"),
    path("signup/", SignupView.as_view(), name="signup"),
    path("verify/<str:key>", complete_verification, name="complete-verification"),
]
