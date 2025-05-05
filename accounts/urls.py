from django.urls import path
from . import views

urlpatterns = [
    path('', views.landing_page, name='landing_page'),
    path('interest/', views.interest_form, name='interest_form'),
    path('signup/', views.signup_form, name='signup_form'),
    path('thank-you/', views.thank_you_page, name='thank_you'),
]