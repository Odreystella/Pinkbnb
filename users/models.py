import uuid
from django.utils.translation import gettext_lazy as _
from django.core.mail import send_mail
from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.html import strip_tags
from django.template.loader import render_to_string
from django.urls import reverse


class User(AbstractUser):

    """Custom User Model"""

    SELECT_GENDER = "Select Gender"
    GENDER_MALE = "male"
    GENDER_FEMALE = "female"
    GENDER_OTHER = "other"

    GENDER_CHOICES = (
        (GENDER_MALE, _("Male")),
        (GENDER_FEMALE, _("Female")),
        (GENDER_OTHER, _("Other")),
    )

    LANGUAGE_ENGLISH = "en"
    LANGUAGE_KOREAN = "kr"

    LANGUAGE_CHOICES = (
        (LANGUAGE_ENGLISH, _("English")),
        (LANGUAGE_KOREAN, _("Korean")),
    )

    CURRENCY_USD = "usd"
    CURRENCY_KRW = "krw"

    CURRENCY_CHOICES = (
        (CURRENCY_USD, "USD"),
        (CURRENCY_KRW, "KRW"),
    )

    LOGIN_EMAIL = "email"
    LOGIN_GITHUB = "github"
    LOGIN_KAKAO = "kakao"

    LOGIN_CHOICES = (
        (LOGIN_EMAIL, _("Email")),
        (LOGIN_GITHUB, _("Github")),
        (LOGIN_KAKAO, _("Kakao")),
    )
    

    # USERNAME_FIELD = "email"
    # REQUIRED_FIELDS = ()
    # email = models.EmailField(max_length=150, unique=True)

    avatar = models.ImageField(_("avatar"), upload_to="avatars", blank=True)
    gender = models.CharField(_("gender"), choices=GENDER_CHOICES, max_length=20, blank=True, default=GENDER_OTHER)
    bio = models.TextField(_("bio"), blank=True)
    birthdate = models.DateField(_("birthdate"), blank=True, null=True)
    language = models.CharField(_("language"), choices=LANGUAGE_CHOICES, max_length=2, blank=True, default=LANGUAGE_KOREAN)
    currency = models.CharField(_("currency"), choices=CURRENCY_CHOICES, max_length=3, blank=True, default=CURRENCY_KRW)
    superhost = models.BooleanField(_("superhost"), default=False)
    email_verified = models.BooleanField(_("email_verified"), default=False)
    email_secret = models.CharField(_("email_secret"), max_length=20, default="", blank=True)
    login_method = models.CharField(_("login_method"), max_length=50, choices=LOGIN_CHOICES, default=LOGIN_EMAIL)

    def __str__(self):
        return self.username

    def get_absolute_url(self):
        return reverse('users:profile', kwargs={'pk': self.pk})

    def verify_email(self):
        if self.email_verified is False:
            secret = uuid.uuid4().hex[:20]
            self.email_secret = secret
            html_message = render_to_string("emails/verify_email.html", {"secret": secret, "username": self.email})
            send_mail(
                _('Verify Pinkbnb Account'),  
                strip_tags(html_message),
                settings.EMAIL_HOST_USER,  
                [self.email],  
                fail_silently=False, 
                html_message=html_message
            )
            self.save()
            print("이메일 보냄")
        return
