from django.views import View
from django.views.generic import FormView
from django.contrib.auth import authenticate, login, logout
from django.urls import reverse_lazy, reverse
from django.shortcuts import render, redirect
from .forms import LoginForm, SignupForm
from .models import User

# View 상속하는 경우
# class LoginView(View):

#     def get(self, request):
#         form = LoginForm(initial={"email": "ojo1001@naver.com"})
#         return render(request, "users/login.html", {"form": form})

#     def post(self, request):
#         form = LoginForm(request.POST)
#         if form.is_valid():
#             email = form.cleaned_data.get("email")
#             password = form.cleaned_data.get("password")
#             user = authenticate(request, username=email, password=password)
#             if user is not None:
#                 login(request, user)
#                 return redirect(reverse("core:home"))

#         return render(request, "users/login.html", {"form": form})

# FormView 상속하는 경우
class LoginView(FormView):

    template_name = "users/login.html"
    form_class = LoginForm
    success_url = reverse_lazy("core:home")  # 성공할 때 사용될 수 있게 reverse_lazy 씀
    initial = {"email": "admin@admin.com"}

    def form_valid(self, form):
        # This method is called when valid form data has been POSTed.
        # It should return an HttpResponse.

        email = form.cleaned_data.get("email")
        password = form.cleaned_data.get("password")
        user = authenticate(self.request, username=email, password=password)
        if user is not None:
            login(self.request, user)
        return super().form_valid(form)  # get_success_url 호출함


def log_out(request):
    logout(request)
    return redirect(reverse("core:home"))


class SignupView(FormView):
    template_name = "users/signup.html"
    form_class = SignupForm
    success_url = reverse_lazy("core:home")  
    initial = {
        "first_name": "Stella",
        "last_name": "Odrey",
        "email": "ojo1001@naver.com",
    }

    def form_valid(self, form):
        form.save()         # form.is_valid() 가 True라면 save
        email = form.cleaned_data.get("email")
        password = form.cleaned_data.get("password")
        user = authenticate(self.request, username=email, password=password)
        if user is not None:
            login(self.request, user)
        user.verify_email()
        return super().form_valid(form)


def complete_verification(request, key):
    try:
        user = User.objects.get(email_secret=key)
        user.email_verified = True
        user.email_secret = ""
        user.save()
        # To do: add sucess message
    except User.DoesNotExist:
        # To do: add error message 
        pass
    return redirect(reverse("core:home"))