from django import forms
from .models import User

class LoginForm(forms.Form):

    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput)

    def clean_email(self):
        email = self.cleaned_data.get("email")
        try:
            User.objects.get(username=email)
            print("clean email")
            return email
        except User.DoesNotExist:
            raise forms.ValidationError("User does not exist")

    def clean_password(self):
        email = self.cleaned_data.get("email")
        password = self.cleaned_data.get("password")
        try:
            user = User.objects.get(username=email)
            if user.check_password(password):
                return password
            else:
                raise forms.ValidationError("Password is wrong")
        except User.DoesNotExist:
            pass