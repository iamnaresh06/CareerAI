"""
Authentication Views for CareerAI.

This module handles user registration, login, logout, and the main landing page.
It ensures that authenticated users are redirected appropriately.

Author: Naresh Reddy
"""

from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from core.models import UserProfile


def landing_page(request):
    """
    Renders the public landing page.
    If the user is already logged in, they are redirected to their dashboard.
    """
    if request.user.is_authenticated:
        return redirect('dashboard')
    return render(request, 'core/authentication/landing.html')


def register_view(request):
    """
    Handles user registration with strict validation.
    """
    if request.method == "POST":
        first_name = request.POST.get("first_name")
        last_name = request.POST.get("last_name")
        email = request.POST.get("email", "").strip()
        contact_number = request.POST.get("contact_number", "").strip()
        password = request.POST.get("password")
        confirm_password = request.POST.get("confirm_password")

        # 1. Validation: Passwords match and length
        if len(password) < 8:
            messages.error(request, "Password must be at least 8 characters long.")
            return redirect("register")
            
        if password != confirm_password:
            messages.error(request, "Passwords do not match.")
            return redirect("register")

        # 2. Validation: Email Format & Domain
        import re
        email_regex = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        if not re.match(email_regex, email):
            messages.error(request, "Invalid email format.")
            return redirect("register")
        
        # Check for common typos/bad extensions
        invalid_extensions = ['.ocm', '.cm', '.con', '.netm']
        if any(email.endswith(ext) for ext in invalid_extensions):
            messages.error(request, "It looks like your email extension (e.g. .com) is incorrect.")
            return redirect("register")

        if User.objects.filter(email=email).exists():
            messages.error(request, "This email is already registered.")
            return redirect("register")

        # 3. Validation: Contact Number (10 digits)
        if not contact_number.isdigit() or len(contact_number) != 10:
            messages.error(request, "Contact number must be exactly 10 digits.")
            return redirect("register")

        # Create User (Username = Email)
        try:
            new_user = User.objects.create_user(
                username=email, # Shadow username
                email=email,
                password=password,
                first_name=first_name,
                last_name=last_name
            )
            # Update Profile with contact number (Signal creates profile, we update it)
            profile = new_user.userprofile
            profile.contact_number = contact_number
            profile.save()
            
            messages.success(request, "Account created successfully! Please login.")
            return redirect("login")
        except Exception as e:
            messages.error(request, f"Error creating account: {e}")
            return redirect("register")

    return render(request, "core/authentication/register.html")


def login_view(request):
    """
    Handles user login using Email. 
    Supports both new users (email=username) and legacy users (email lookup).
    """
    if request.method == "POST":
        email_input = request.POST.get('email', '').strip()
        password = request.POST.get('password')

        # 1. Try to find the user by email first
        try:
            user_obj = User.objects.get(email__iexact=email_input)
            actual_username = user_obj.username
        except User.DoesNotExist:
            # Maybe they entered their username in the email field
            actual_username = email_input

        # 2. Authenticate using the resolved username
        user = authenticate(request, username=actual_username, password=password)

        if user is not None:
            login(request, user)
            if user.is_superuser or user.is_staff:
                return redirect('admin_dashboard')
            return redirect('dashboard')
        else:
            messages.error(request, "Invalid email or password")
            return redirect('login')

    return render(request, 'core/authentication/login.html')


def logout_view(request):
    """
    Logs out the user and redirects to the login page.
    """
    logout(request)
    return redirect('login')

def about_page(request):
    """
    Renders the public 'About Us' page.
    """
    return render(request, 'core/authentication/about.html')

def privacy_policy(request):
    """
    Renders the professional Privacy Policy page.
    """
    return render(request, 'core/authentication/privacy.html')

def terms_conditions(request):
    """
    Renders the professional Terms & Conditions page.
    """
    return render(request, 'core/authentication/terms.html')

def refund_policy(request):
    """
    Renders the professional Refund Policy page.
    """
    return render(request, 'core/authentication/refund.html')

@login_required(login_url='login')
def careers_page(request):
    """
    Renders the Careers page.
    """
    return render(request, 'core/authentication/careers.html')

def roadmaps_view(request):
    """
    Renders the Career Roadmaps page.
    """
    return render(request, 'core/roadmaps.html')

@login_required(login_url='login')
def expert_bundle_view(request):
    """
    Renders the detailed step-by-step process for the Placement Success Bundle.
    """
    return render(request, 'core/services/expert_bundle.html')

@login_required(login_url='login')
def tech_tuition_view(request):
    """
    Renders the detailed step-by-step process for Online Tech Tuition (Hybrid Model).
    """
    return render(request, 'core/services/tech_tuition.html')

@login_required(login_url='login')
def capstone_pro_view(request):
    """
    Renders the detailed step-by-step process for Capstone Project Pro (Final Year Projects).
    """
    return render(request, 'core/services/capstone_pro.html')

@login_required(login_url='login')
def profile_view(request):
    """
    Allows authenticated users to view and update their profile details and photo.
    """
    user = request.user
    # Get or create the user profile
    profile, created = UserProfile.objects.get_or_create(user=user)

    if request.method == "POST":
        first_name = request.POST.get("first_name")
        last_name = request.POST.get("last_name")
        email = request.POST.get("email")
        profile_image = request.FILES.get("profile_image")

        # Basic email uniqueness check if email was changed
        if email and email != user.email:
            if User.objects.filter(email=email).exists():
                messages.error(request, "This email is already in use by another account.")
                return redirect('profile')

        user.first_name = first_name
        user.last_name = last_name
        if email:
            user.email = email
        user.save()

        # Update profile fields
        profile.contact_number = request.POST.get("contact_number")
        
        # Update profile image and resume if provided
        if profile_image:
            profile.profile_image = profile_image
        if request.FILES.get("resume"):
            profile.resume = request.FILES.get("resume")
        profile.save()
        
        messages.success(request, "Your profile has been updated successfully!")
        return redirect('profile')

    return render(request, 'core/authentication/profile.html', {
        'user': user,
        'profile': profile
    })

from core.models import ServiceBooking

@login_required(login_url='login')
def book_service(request):
    """
    Handles bookings for offline services from the dashboard.
    """
    if request.method == "POST":
        service_type = request.POST.get("service_type", "")
        phone_number = request.POST.get("phone_number", "").strip()
        preferred_tech = request.POST.get("preferred_tech", "").strip()
        contact_time = request.POST.get("contact_time", "").strip()
        payment_mode = request.POST.get("payment_mode", "ONE_TIME")
        
        if not phone_number:
            messages.error(request, "Phone number is required for booking.")
            return redirect("dashboard")

        # Capture additional notes (EMI interest, Paper publication, etc.)
        notes = []
        if request.POST.get("need_paper"):
            notes.append("Needs Research Paper Publication")
        
        notes_str = ", ".join(notes) if notes else None

        ServiceBooking.objects.create(
            user=request.user,
            service_type=service_type,
            phone_number=phone_number,
            preferred_tech=preferred_tech,
            contact_time=contact_time,
            payment_mode=payment_mode,
            notes=notes_str
        )

        messages.success(request, "Your booking request has been successfully captured! Our team will contact you shortly.")
        return redirect("dashboard")

    return redirect("dashboard")
