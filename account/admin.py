from django.contrib import admin
from .models import Customer


class UserBaseAdmin(admin.ModelAdmin):
    """
    Customizes the admin interface for user base model.
    """
    list_display = ('user_name', 'email', 'profile_image_thumbnail')

    def profile_image_thumbnail(self, obj):
        """
        Renders a thumbnail of the user's profile image.
        """
        if obj.profile_image:
            return ('<img src="%s" width="50" height="50" />' %
                    obj.profile_image.url)
        else:
            return 'No image'
    profile_image_thumbnail.allow_tags = True


admin.site.register(Customer)
