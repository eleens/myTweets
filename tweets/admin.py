from django.contrib import admin

# Register your models here.
from models import Tweet, HashTag
from user_profile.models import UserFollowers

class TweetAdmin(admin.ModelAdmin):
    list_display = ('user', 'text', 'create_date')
    list_filter = ('user',)
    search_fields = ('text',)
    ordering = ('-create_date',)

admin.site.register(Tweet, TweetAdmin)
admin.site.register(HashTag)
admin.site.register(UserFollowers)
