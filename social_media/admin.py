from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import *


admin.site.unregister(User)

@admin.register(User)
class CustomUserAdmin(UserAdmin):
    readonly_fields = ("id",)

    def __init__(self, model, admin_site):
        super().__init__(model, admin_site)
        self.list_display = ("id",) + self.list_display

admin.site.register(Account, AccountAdmin)
admin.site.register(Follow)
admin.site.register(Post)
admin.site.register(Like)
admin.site.register(Dislike)