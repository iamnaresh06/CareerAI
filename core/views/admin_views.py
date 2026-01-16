from django.shortcuts import render
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required, user_passes_test
from core.models import JobPosting, Event

def is_admin(user):
    return user.is_superuser or user.is_staff

@login_required
@user_passes_test(is_admin)
def admin_dashboard(request):
    """
    Admin Dashboard: View all users, recent jobs, events and stats.
    """
    total_users = User.objects.count()
    total_jobs = JobPosting.objects.count()
    total_events = Event.objects.count()
    
    users = User.objects.all().order_by('-date_joined')
    jobs = JobPosting.objects.all().order_by('-posted_at')
    events = Event.objects.all().order_by('-date')
    
    context = {
        'total_users': total_users,
        'total_jobs': total_jobs,
        'total_events': total_events,
        'users': users,
        'jobs': jobs,
        'events': events
    }
    return render(request, 'core/admin_dashboard.html', context)
