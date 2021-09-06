from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from rooms.models import Room
from .models import User


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


class RoomInline(admin.TabularInline):
    model = Room


# 방법 1
@admin.register(User)  # 데코레이터를 붙여 주면 CustomUserAdmin 클래스가 models.User를 사용한다는 의미
class CustomUserAdmin(UserAdmin):

    """Custom User Admin"""

    inlines = (RoomInline,)

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

    list_display = (
        "username",
        "first_name",
        "last_name",
        "email",
        "is_active",
        "language",
        "currency",
        "superhost",
        "is_staff",
        "is_superuser",
    )
    list_filter = UserAdmin.list_filter + ("superhost",)


# admin.site.register(models.User, CustomUserAdmin)  # 방법 2
