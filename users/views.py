import os
from django.utils.html import avoid_wrapping
import requests
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


# pinkbnb -> github
def github_login(request):
    client_id = os.environ.get("GITHUB_CLIENT_ID")
    redirect_uri = "http://127.0.0.1:8000/users/login/github/callback/"
    return redirect(f"https://github.com/login/oauth/authorize?client_id={client_id}&redirect_uri={redirect_uri}")


# github -> pinkbnb
def github_callback(request):
    code = request.GET.get("code", None)
    client_id = os.environ.get("GITHUB_CLIENT_ID")
    client_secret = os.environ.get("GITHUB_CLIENT_SECRET")
    if code is not None:                         # 1. callback으로 code 받았는지 확인
        response = requests.post(
            f"https://github.com/login/oauth/access_token?client_id={client_id}&client_secret={client_secret}&code={code}",
            headers={"Accept": "application/json"}
            )
        response_json = response.json()
        error = response_json.get("error", None)
        if error is not None:                    # 2. 시간 초과, code 두번 이상 사용 등으로 error가 있다면 redirect
            return redirect(reverse("users:login"))
        else:                                    # 3. callback로 받은 code로 access_token 발급 받아서 user api에 접근하기  
            access_token = response_json.get("access_token")
            profile_request = requests.get(
                "https://api.github.com/user", 
                headers={
                    "Authorization": f"token {access_token}",
                    "Accept": "application/json"
                },
            )
            profile_json = profile_request.json() # 4. user 정보 받음
            username = profile_json.get("login", None)
            if username is not None:              # 5. github에 user 정보가 있다면, name, email, bio 가져오기
                name = profile_json.get("name")
                email = profile_json.get("email")
                bio = profile_json.get("bio")
                try:                                     # 6. pinkbnb에 해당 이메일로 이미 유저가 존재하는데, 그 유저가 이미 github의 로그인 인증을 거쳤다면 로그인 시켜주기
                    user = User.objects.get(email=email) 
                    if user.login_method != User.LOGIN_GITHUB: 
                        raise GithubException()                # 6-1. 다른 login_method로 만들어진 유저라면 에러 발생
                              
                except User.DoesNotExist:                # 7. pinkbnb에 해당 이메일의 유저가 없다면 만들어주기
                    user = User.objects.create(
                        username=email, 
                        first_name=name, 
                        email=email,
                        bio=bio,
                        login_method=User.LOGIN_GITHUB,
                    )
                    user.set_unusable_password()
                    user.save()
                login(request, user)
                return redirect(reverse("core:home"))
            else:
                return redirect(reverse("users:login"))

    else:
        return redirect(reverse("users:login"))