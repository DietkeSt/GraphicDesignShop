from django.contrib import admin

from .models import UserBase


class UserBaseAdmin(admin.ModelAdmin):
    list_display = ('user_name', 'email', 'profile_image_thumbnail')  # Add profile image to list display

    def profile_image_thumbnail(self, obj):
        if obj.profile_image:
            return '<img src="%s" width="50" height="50" />' % obj.profile_image.url
        else:
            return 'No image'
    profile_image_thumbnail.allow_tags = True
    

admin.site.register(UserBase)