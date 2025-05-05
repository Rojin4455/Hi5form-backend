from django.contrib import admin
from .models import UserProfile, ReferralSignup, InterestedUser

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'mobile_number', 'age', 'place', 'referral_code', 'extra_tickets', 'created_at')
    search_fields = ('user__username', 'user__email', 'user__first_name', 'place')
    list_filter = ('created_at', 'age')
    readonly_fields = ('referral_code',)

@admin.register(ReferralSignup)
class ReferralSignupAdmin(admin.ModelAdmin):
    list_display = ('referrer', 'referred_user', 'created_at')
    search_fields = ('referrer__user__username', 'referred_user__user__username')
    list_filter = ('created_at',)

@admin.register(InterestedUser)
class InterestedUserAdmin(admin.ModelAdmin):
    list_display = ('email', 'interested', 'created_at')
    search_fields = ('email',)
    list_filter = ('interested', 'created_at')