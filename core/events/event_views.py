"""
Event Views for CareerAI.

This module manages the Events & Hackathons feature:
1. Listing Upcoming Events.
2. Admin Actions: Posting and Deleting Events.

Author: Naresh Reddy
"""

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from core.models import Event

# ==============================
# HELPERS
# ==============================

def is_admin(user):
    """
    Checks if a user has administrative privileges.
    """
    return user.is_superuser or user.is_staff


# ==============================
# VIEWS
# ==============================

@login_required
def event_list(request):
    """
    Displays the Events Board.
    Lists all active events, sorted by upcoming dates.
    """
    # Fetch active events and sort by date (soonest first)
    events = Event.objects.filter(is_active=True).order_by('date')
    return render(request, 'core/events/event_list.html', {'events': events})


@login_required
@user_passes_test(is_admin)
def post_event(request):
    """
    Admin View: Post a new Event or Hackathon.
    """
    if request.method == "POST":
        try:
            Event.objects.create(
                name=request.POST.get('name'),
                event_type=request.POST.get('event_type'),
                description=request.POST.get('description'),
                registration_link=request.POST.get('registration_link'),
                date=request.POST.get('date'),
                location=request.POST.get('location'),
                posted_by=request.user
            )
            
            messages.success(request, "New event posted successfully!")
            return redirect('admin_dashboard')
            
        except Exception as e:
            messages.error(request, f"Error posting event: {e}")
            return redirect('post_event')
        
    return render(request, 'core/events/post_event.html')


@login_required
@user_passes_test(is_admin)
def delete_event(request, event_id):
    """
    Admin View: Delete an Event.
    """
    event = get_object_or_404(Event, id=event_id)
    
    if request.method == "POST":
        event.delete()
        messages.success(request, "Event deleted successfully.")
        
    return redirect('admin_dashboard')
