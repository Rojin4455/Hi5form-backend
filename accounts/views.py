import uuid
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib import messages
from django.urls import reverse
from django.http import HttpResponse
from .models import UserProfile, ReferralSignup, InterestedUser
from .forms import InterestForm, SignupForm

def landing_page(request):
    """Landing page view with HI5 promotional content"""
    return render(request, 'subscription/landing.html')

def interest_form(request):
    """Interest form to check if users are interested in the subscription model"""
    if request.method == 'POST':
        form = InterestForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            interested = form.cleaned_data['interested']
            
            # Save the interest data
            InterestedUser.objects.create(
                email=email,
                interested=interested
            )
            
            if interested:
                # If user is interested, redirect to signup form
                return redirect(reverse('signup_form') + f'?email={email}')
            else:
                # If not interested, thank them and return to landing page
                messages.info(request, "Thank you for your feedback!")
                return redirect('landing_page')
    else:
        form = InterestForm()
    
    return render(request, 'subscription/interest_form.html', {'form': form})

def signup_form(request):
    """User signup form with all required fields"""
    # Check for referral code
    referral_code = request.GET.get('ref', None)
    email = request.GET.get('email', '')
    
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            # Create the user
            user = User.objects.create_user(
                username=form.cleaned_data['email'],
                email=form.cleaned_data['email'],
                password=form.cleaned_data['password'],
                first_name=form.cleaned_data['name'],
            )
            
            # Create the user profile
            profile = UserProfile.objects.create(
                user=user,
                age=form.cleaned_data['age'],
                mobile_number=form.cleaned_data['mobile_number'],
                place=form.cleaned_data['place'],
            )
            
            # Handle referral if exists
            if referral_code:
                try:
                    referrer_profile = UserProfile.objects.get(referral_code=uuid.UUID(referral_code))
                    # Create referral relationship
                    ReferralSignup.objects.create(
                        referrer=referrer_profile,
                        referred_user=profile
                    )
                    messages.success(request, "You've been successfully referred! Your friend will receive credit for this referral.")
                except (UserProfile.DoesNotExist, ValueError):
                    messages.error(request, "Invalid referral code.")
            
            # Redirect to thank you page with the referral code
            return redirect(reverse('thank_you') + f'?ref={profile.referral_code}')
    else:
        # Pre-fill email if coming from interest form
        initial_data = {'email': email} if email else {}
        form = SignupForm(initial=initial_data)
    
    return render(request, 'subscription/signup_form.html', {
        'form': form,
        'referral_code': referral_code
    })

def thank_you_page(request):
    """Thank you page with referral information"""
    referral_code = request.GET.get('ref', '')
    referral_url = request.build_absolute_uri(reverse('signup_form') + f'?ref={referral_code}')
    
    return render(request, 'subscription/thank_you.html', {
        'referral_code': referral_code,
        'referral_url': referral_url
    })