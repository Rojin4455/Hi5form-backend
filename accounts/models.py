import uuid
from django.db import models
from django.contrib.auth.models import User

class UserProfile(models.Model):
    """User profile model extending Django's User model"""
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    mobile_number = models.CharField(max_length=15)
    age = models.IntegerField()
    place = models.CharField(max_length=255)
    referral_code = models.UUIDField(default=uuid.uuid4, unique=True, editable=False)
    extra_tickets = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.user.username}'s Profile"
    
    def get_referral_url(self):
        """Generate a referral URL"""
        return f"/signup/?ref={self.referral_code}"

class ReferralSignup(models.Model):
    """Model to track referrals"""
    referrer = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='referrals')
    referred_user = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='referred_by')
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ('referrer', 'referred_user')
    
    def __str__(self):
        return f"{self.referrer.user.username} referred {self.referred_user.user.username}"
    
    def save(self, *args, **kwargs):
        """Override save to update referrer's extra tickets"""
        super().save(*args, **kwargs)
        # Count referrals and update extra tickets
        referral_count = ReferralSignup.objects.filter(referrer=self.referrer).count()
        self.referrer.extra_tickets = referral_count // 5  # One ticket for every 5 referrals
        self.referrer.save()

class InterestedUser(models.Model):
    """Model to track users who expressed interest but didn't complete signup"""
    email = models.EmailField(unique=True)
    interested = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.email