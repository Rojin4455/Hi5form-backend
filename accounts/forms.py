from django import forms
from django.contrib.auth.models import User
from django.core.validators import RegexValidator
from .models import UserProfile, InterestedUser

class InterestForm(forms.ModelForm):
    """Form to capture initial interest"""
    interested = forms.BooleanField(
        label="Are you interested in subscribing to HI5 Pass - Watch 5 Movies for ₹555/month?",
        required=True
    )
    
    class Meta:
        model = InterestedUser
        fields = ['email', 'interested']

class SignupForm(forms.Form):
    """User signup form with all required fields"""
    name = forms.CharField(max_length=100)
    age = forms.IntegerField(min_value=13, max_value=120)
    mobile_number = forms.CharField(
        max_length=15,
        validators=[
            RegexValidator(
                regex=r'^\+?1?\d{10,15}$',
                message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed."
            )
        ]
    )
    email = forms.EmailField()
    place = forms.CharField(max_length=255)
    password = forms.CharField(widget=forms.PasswordInput)
    confirm_password = forms.CharField(widget=forms.PasswordInput)
    
    def clean(self):
        """Validate that both passwords match"""
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')
        
        if password and confirm_password and password != confirm_password:
            raise forms.ValidationError("Passwords do not match")
        
        return cleaned_data
    
    def clean_email(self):
        """Check if email already exists in User model"""
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("This email is already registered")
        return email