from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from jangela.models import (
    ErabiltzaileaModel,
    ErreserbaModel,
    IkasleaModel,
    IkasturtekoErreserbaModel,
    MenuaModel,
    OrdainketaModel,
)


@admin.register(ErabiltzaileaModel)
class ErabiltzaileaAdmin(UserAdmin):
    """UserAdmin egokitua: emaila erabiltzen da username-aren ordez."""

    ordering = ("email",)
    list_display = ("email", "first_name", "last_name", "rola", "beganoa", "is_active")
    list_filter = ("rola", "beganoa", "is_active", "is_staff")
    search_fields = ("email", "first_name", "last_name")
    fieldsets = (
        (None, {"fields": ("email", "password")}),
        ("Datu pertsonalak", {"fields": ("first_name", "last_name", "rola", "beganoa")}),
        ("Baimenak", {"fields": ("is_active", "is_staff", "is_superuser", "groups", "user_permissions")}),
        ("Datak", {"fields": ("last_login", "date_joined")}),
    )
    add_fieldsets = (
        (None, {
            "classes": ("wide",),
            "fields": ("email", "rola", "password1", "password2"),
        }),
    )


admin.site.register(IkasleaModel)
admin.site.register(IkasturtekoErreserbaModel)
admin.site.register(ErreserbaModel)
admin.site.register(OrdainketaModel)
admin.site.register(MenuaModel)
