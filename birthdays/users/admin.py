from django.contrib import admin

from .models import Follow


@admin.register(Follow)
class FollowModelAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'author')
    fields = ('user', 'author')
