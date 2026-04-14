"""
Admin Views for CareerAI.

This module provides the administrative dashboard to oversee the platform:
1. User Management Stats.
2. Job Listing Management.
3. Event Listing Management.

Author: Naresh Reddy
"""

from django.db.models import Q
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required, user_passes_test
from core.models import JobPosting, Event, UserProfile, ServiceBooking

# ==============================
# PERMISSION HELPERS
# ==============================

def is_admin(user):
    """
    Checks if a user has administrative privileges.
    """
    return user.is_superuser or user.is_staff


# ==============================
# ADMIN VIEWS
# ==============================

@login_required
@user_passes_test(is_admin)
def admin_dashboard(request):
    """
    Renders the central Admin Dashboard with Search.
    """
    query = request.GET.get('q', '')
    
    # Quick Statistics
    total_users = User.objects.count()
    total_jobs = JobPosting.objects.count()
    total_events = Event.objects.count()
    total_bookings = ServiceBooking.objects.count()
    
    # User Filtering (Search)
    if query:
        users = User.objects.filter(
            Q(username__icontains=query) | 
            Q(email__icontains=query) | 
            Q(userprofile__student_id__icontains=query)
        ).distinct().order_by('-date_joined')
    else:
        users = User.objects.all().order_by('-date_joined')
    
    jobs = JobPosting.objects.all().order_by('-posted_at')
    events = Event.objects.all().order_by('-date')
    bookings = ServiceBooking.objects.all().order_by('-created_at')
    
    context = {
        'total_users': total_users,
        'total_jobs': total_jobs,
        'total_events': total_events,
        'total_bookings': total_bookings,
        'users': users,
        'jobs': jobs,
        'events': events,
        'bookings': bookings,
        'query': query
    }
    
    return render(request, 'core/administration/admin_dashboard.html', context)


@login_required
@user_passes_test(is_admin)
def admin_user_profile(request, user_id):
    """
    Allows admin to view any user's profile and download their resume.
    """
    target_user = get_object_or_404(User, id=user_id)
    profile, created = UserProfile.objects.get_or_create(user=target_user)
    
    return render(request, 'core/administration/admin_user_profile.html', {
        'target_user': target_user,
        'profile': profile
    })


@login_required
@user_passes_test(is_admin)
def update_booking_status(request, booking_id):
    """
    Updates the status of a specific service booking from the Admin Dashboard.
    """
    if request.method == "POST":
        booking = get_object_or_404(ServiceBooking, id=booking_id)
        new_status = request.POST.get("status")
        if new_status:
            booking.status = new_status
            booking.save()
    return redirect('admin_dashboard')
