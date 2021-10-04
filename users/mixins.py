from django.contrib import messages
from django.urls import reverse_lazy, reverse
from django.shortcuts import redirect
from django.contrib.auth.mixins import UserPassesTestMixin, LoginRequiredMixin


class LoggedOutOnlyView(UserPassesTestMixin):

    """
    Deny a request with a permission error if the test_func() method returns
    False.
    test_func()가 False여야 handle_no_permission()이 실행됨
    """

    def test_func(self):      # 로그인한 유저가 로그인 페이지로 가면 false를 반환해서 core:home으로 리다이렉트
        return not self.request.user.is_authenticated

    def handle_no_permission(self):
        messages.error(self.request, "Can't go there")
        return redirect(reverse("core:home"))


class LoggedInOnlyView(LoginRequiredMixin):

    login_url = reverse_lazy("users:login")


class EmailLoginOnlyView(UserPassesTestMixin):

    def test_func(self):
        return self.request.user.login_method == "email"

    def handle_no_permission(self):
        messages.error(self.request, "Can't go there")
        return redirect(reverse("core:home"))