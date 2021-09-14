from django.contrib import admin
from django.contrib.admin.options import InlineModelAdmin
from django.utils.html import mark_safe
from .models import Room, RoomType, Amenity, Facility, HouseRule, Photo


@admin.register(RoomType, Amenity, Facility, HouseRule)
class ItemAdmin(admin.ModelAdmin):

    """Item Admin Definition"""

    list_display = (
        "name",
        "used_by",
    )

    def used_by(self, obj):
        return obj.rooms.count()


class PhotoInline(admin.TabularInline):
    model = Photo


@admin.register(Room)
class RoomAdmin(admin.ModelAdmin):

    """Room Admin Definition"""

    inlines = (PhotoInline,)

    fieldsets = (
        (
            "Basic Info",
            {
                "fields": (
                    "name",
                    "description",
                    "room_type",
                    "country",
                    "city",
                    "address",
                    "price",
                )
            },
        ),
        ("Times", {"fields": ("check_in", "check_out", "instant_book")}),
        ("Spaces", {"fields": ("guests", "beds", "bedrooms", "baths")}),
        (
            "More About the Space",
            {
                "classes": ("collapse",),
                "fields": (
                    "amenities",
                    "facilities",
                    "house_rules",
                ),
            },
        ),
        ("Last Details", {"fields": ("host",)}),
    )
    raw_id_fields = ("host",)
    list_display = (
        "name",
        "country",
        "city",
        "room_type",
        "price",
        "guests",
        "beds",
        "baths",
        "bedrooms",
        "check_in",
        "check_out",
        "instant_book",
        "count_amenities",
        "count_photos",
        "total_rating",
    )
    ordering = ("instant_book",)
    list_filter = (
        "instant_book",
        "host__superhost",
        "room_type",
        "amenities",
        "facilities",
        "house_rules",
        "city",
        "country",
    )
    search_fields = (
        "city",
        "^host__username",
        "name",
    )
    filter_horizontal = (
        "amenities",
        "facilities",
        "house_rules",
    )

    # admin에서 모델 인스턴스를 저장할 때 호출되는 메서드
    # 결과적으로 models.py에서 super().save() 해줘야 저장됨
    # 예를 들어, send_mail()코드를 넣으면 누군가 admin에서 모델 변경하면 메일이 날라오게 할 수도 있음
    def save_model(self, request, obj, form, change):
        # if (
        #     obj.host != request.user
        # ):  # admin에서 room의 호스트와 로그인한 사람이 같을때만 모델 변경이 가능하게끔 조건 걸 수 있음
        super().save_model(request, obj, form, change)  # obj.save() 함

    # admin안의 함수는 2개의 파라미터를 가짐, self : RoomAdmin class, obj : room instance
    def count_amenities(self, obj):
        return obj.amenities.count()

    count_amenities.short_description = "Amenities Count"

    def count_photos(self, obj):
        return obj.photos.count()

    count_photos.short_description = "Photo Count"


@admin.register(Photo)
class PhotoAdmin(admin.ModelAdmin):

    """Photo Admin Definition"""

    list_display = ("__str__", "get_thumbnail")

    def get_thumbnail(self, obj):
        return mark_safe(f"<img width='50px' height='50px' src='{obj.file.url}' />")

    get_thumbnail.short_description = "Thumbnail"
