import os
import requests
from django.views.generic.base import RedirectView
from django.views import View
from django.contrib.auth.views import PasswordChangeView
from django.views.generic import FormView, DetailView, UpdateView
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.core.files.base import ContentFile
from django.urls import reverse_lazy, reverse
from django.shortcuts import render, redirect
from .forms import LoginForm, SignupForm, ProfileForm
from .models import User
from .mixins import LoggedOutOnlyView, LoggedInOnlyView, EmailLoginOnlyView

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
class LoginView(LoggedOutOnlyView, FormView):

    template_name = "users/login.html"
    form_class = LoginForm
    # success_url = reverse_lazy("core:home")  # 클래스안에서는 reverse_lazy 씀
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
    
    def get_success_url(self):
        next_arg = self.request.GET.get("next")
        if next_arg is not None:
            return next_arg
        else:
            return reverse("core:home")


def log_out(request):
    logout(request)
    messages.info(request, "See you later")
    return redirect(reverse("core:home"))


class SignupView(FormView):
    template_name = "users/signup.html"
    form_class = SignupForm
    success_url = reverse_lazy("core:home")  

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


class GithubException(Exception):
    pass


# pinkbnb -> github
def github_login(request):
    client_id = os.environ.get("GITHUB_CLIENT_ID")
    redirect_uri = "http://127.0.0.1:8000/users/login/github/callback/"
    return redirect(f"https://github.com/login/oauth/authorize?client_id={client_id}&redirect_uri={redirect_uri}")


# when user clicked accept, github -> pinkbnb
def github_callback(request):
    try: 
        code = request.GET.get("code", None)
        client_id = os.environ.get("GITHUB_CLIENT_ID")
        client_secret = os.environ.get("GITHUB_CLIENT_SECRET")
        if code is not None:                         # 1. callback으로 code 받았는지 확인
            token_request = requests.post(
                f"https://github.com/login/oauth/access_token?client_id={client_id}&client_secret={client_secret}&code={code}",
                headers={"Accept": "application/json"}
                )
            token_json = token_request.json()
            error = token_json.get("error", None)
            if error is not None:                    # 2. 시간 초과, code 두번 이상 사용 등으로 error가 있다면 redirect / json에 에러가 있는지 체크
                raise GithubException("Can't get access token")
            else:                                    # 3. 에러가 없으면, callback로 받은 code로 access_token 발급 받아서  
                access_token = token_json.get("access_token")
                profile_request = requests.get(      # 3. github api에 requests 보내기
                    "https://api.github.com/user", 
                    headers={
                        "Authorization": f"token {access_token}",
                        "Accept": "application/json"
                    },
                )
                profile_json = profile_request.json() # 4. response로 user 정보 받음
                username = profile_json.get("login", None)
                if username is not None:              # 5. github에 user 정보가 있다면, name, email, bio 가져오기
                    name = profile_json.get("name")
                    email = profile_json.get("email")
                    bio = profile_json.get("bio")
                    try:                                     # 6. pinkbnb에 해당 이메일로 이미 유저가 존재하는데, 그 유저가 이미 github의 로그인 인증을 거쳤다면 로그인 시켜주기
                        user = User.objects.get(email=email) 
                        if user.login_method != User.LOGIN_GITHUB: 
                            raise GithubException(f"Please log in with: {user.login_method}") # 6-1. 다른 login_method로 만들어진 유저라면 에러 발생
                                
                    except User.DoesNotExist:                # 7. pinkbnb에 해당 이메일의 유저가 없다면 만들어주기
                        user = User.objects.create(
                            username=email, 
                            first_name=name, 
                            email=email,
                            bio=bio,
                            login_method=User.LOGIN_GITHUB,
                            email_verified=True,
                        )
                        user.set_unusable_password()
                        user.save()

                    login(request, user)
                    messages.success(request, f"Welcome back {user.first_name}")
                    
                    return redirect(reverse("core:home"))
                else:                                        # 8. user 정보가 없다면 에러 발생
                    raise GithubException("Can't get your profile")
        else:
            raise GithubException("Can't get code")
    except GithubException as e:
        messages.error(request, e)
        return redirect(reverse("users:login"))     


class KakaoException(Exception):
    pass


def kakao_login(request):
    client_id = os.environ.get("KAKAO_CLIENT_ID")
    redirect_uri = "http://127.0.0.1:8000/users/login/kakao/callback/"

    return redirect(f"https://kauth.kakao.com/oauth/authorize?client_id={client_id}&redirect_uri={redirect_uri}&response_type=code")
    

def kakao_callback(request):
    try:
        # access_token 받기
        code = request.GET.get("code")
        client_id = os.environ.get("KAKAO_CLIENT_ID")
        redirect_uri = "http://127.0.0.1:8000/users/login/kakao/callback/"
        token_request = requests.post(
            f"https://kauth.kakao.com/oauth/token?grant_type=authorization_code&client_id={client_id}&code={code}&redirect_uri={redirect_uri}",
           )
        token_json = token_request.json()
        # print(token_json)
        error = token_json.get("error", None)
        if error is not None:
            raise KakaoException("Can't get authorization code.")
        access_token = token_json.get("access_token")
        
        # 카카오 API 호출하기
        profile_request = requests.get(
            "https://kapi.kakao.com/v2/user/me",
            headers={"Authorization": f"Bearer {access_token}"}
            )
        profile_json = profile_request.json()
        # print(profile_json)
        email = profile_json.get("kakao_account").get("email", None)
        if email is None:
            raise KakaoException("Plase also give me your email")
        nickname = profile_json.get("properties").get("nickname")
        profile_img = profile_json.get("properties").get("profile_image")
        # print(profile_img)
        try:
            user = User.objects.get(email=email)
            if user.login_method != User.LOGIN_KAKAO:
                raise KakaoException(f"Please log in with: {user.login_method}")
                
        # API로 가져온 사용자 정보로 유저 생성하기
        except User.DoesNotExist:
            user = User.objects.create(
                username=email,
                first_name=nickname,
                email=email,
                login_method=User.LOGIN_KAKAO,
                email_verified=True,
            )
            user.set_unusable_password()
            user.save()
            if profile_img is not None:
                photo_request = requests.get(profile_img)
                user.avatar.save(f"{nickname}-avatar", ContentFile(photo_request.content))
        
        login(request, user)
        messages.success(request, f"Welcome back {user.first_name}")
        return redirect(reverse("core:home"))

    except KakaoException as e:
        messages.error(request, e)
        return redirect(reverse("users:login"))


class UserProfileView(DetailView):

    model = User
    context_object_name = "user_obj"


# UpdateView를 사용하면 form을 따로 정의하지 않아도 됨
# form에 많은 컨트롤이 필요하다면 따로 사용하는게 좋음
class UpdateProfileView(LoggedInOnlyView, SuccessMessageMixin, UpdateView):
    
    model = User
    form_class = ProfileForm
    template_name = "users/update-profile.html"
    # fields = (
    #     "first_name",
    #     "last_name",
    #     "gender",
    #     "bio",
    #     "birthdate",
    #     "language",
    #     "currency",
    # )
    success_message = "Profile Updated"

    def get_object(self, queryset=None):
        return self.request.user

    def get_form(self, form_class=None):
        form = super().get_form(form_class=form_class)
        return form

  
class UpdatePasswordView(LoggedInOnlyView, EmailLoginOnlyView, SuccessMessageMixin,PasswordChangeView):

    template_name = "users/update_password.html"
    success_message = "Password Updated"


    def get_form(self, form_class=None):
        form = super().get_form(form_class=form_class)
        form.fields["old_password"].widget.attrs = {"placeholder": "Current password"}
        form.fields["new_password1"].widget.attrs = {"placeholder": "New password"}
        form.fields["new_password2"].widget.attrs = {"placeholder": "Confirm new password"}
        return form

    def get_success_url(self):
        return self.request.user.get_absolute_url()


@login_required
def switch_hosting(request):

    # 세션 삭제하는 방법 1
    # request.session.pop("is_hosting", True)

    # 방법 2
    try:
        del request.session["is_hosting"]
    except KeyError:
        request.session["is_hosting"] = True
        
    return redirect(reverse("core:home"))