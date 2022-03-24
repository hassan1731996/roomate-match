from django.contrib import admin
from .models import UserPosts, UserRegistration, ImageModel, UserContacts


class PostsImageAdmin(admin.ModelAdmin):
    list_display = ('image_tag',)


admin.site.register(UserPosts)
admin.site.register(UserRegistration)
admin.site.register(UserContacts)
admin.site.register(ImageModel, PostsImageAdmin)
