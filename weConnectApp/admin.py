from django.contrib import admin
from .models import Profile, Post, LikePost, FollowersCount

# Register your models here.

class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'name', 'about')

class PostAdmin(admin.ModelAdmin):
    list_display = ('caption',)

class LikePostAdmin(admin.ModelAdmin):
   list_display = ('post_id', 'username')

admin.site.register(Profile, ProfileAdmin)
admin.site.register(Post, PostAdmin)
admin.site.register(LikePost, LikePostAdmin)
admin.site.register(FollowersCount)
