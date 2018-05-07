from django.contrib import admin

from .models import Category, Nickname


class NicknameAdmin(admin.ModelAdmin):
    model = Nickname
    list_display = ('nickname', 'category', 'info')


admin.site.register(Category)
admin.site.register(Nickname, NicknameAdmin)
