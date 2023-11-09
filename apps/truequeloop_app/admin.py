from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as AuthUserAdmin
from django.contrib.auth.models import User

from .models import Profile, Community, Trade, Location, TradeImages, Message, OpenChat, CommunityRequest


# Register your models here.

class UserProfileInline(admin.StackedInline):
    model = Profile
    can_delete = False


class AccountsUserAdmin(AuthUserAdmin):
    inlines = [UserProfileInline]


admin.site.unregister(User)
admin.site.register(User, AccountsUserAdmin)
admin.site.register(Community)
admin.site.register(Trade)
admin.site.register(Location)
admin.site.register(TradeImages)
admin.site.register(OpenChat)
admin.site.register(CommunityRequest)

