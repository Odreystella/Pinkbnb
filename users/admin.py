from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from . import models


# admin.ModelAdmin을 상속받는 경우
# @admin.register(models.User)
# class CustomUserAdmin(admin.ModelAdmin):

#     """ Custom User Admin """

#     list_display = ("username", "email", "gender", "language", "currency", "superhost")
#     list_filter = (
#         "language",
#         "currency",
#         "superhost",
#     )

# 방법 1
@admin.register(models.User)  # 데코레이터를 붙여 주면 CustomUserAdmin 클래스가 models.User를 사용한다는 의미
class CustomUserAdmin(UserAdmin):

    """Custom User Admin"""

    fieldsets = UserAdmin.fieldsets + (
        (
            "Custom Profile",
            {
                "fields": (
                    "avatar",
                    "gender",
                    "bio",
                    "birthdate",
                    "language",
                    "currency",
                    "superhost",
                )
            },
        ),
    )


# admin.site.register(models.User, CustomUserAdmin)  # 방법 2
