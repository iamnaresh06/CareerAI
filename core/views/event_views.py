from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from core.models import Event

def is_admin(user):
    return user.is_superuser or user.is_staff

@login_required
def event_list(request):
    """
    Displays a list of all active events and hackathons.
    """
    events = Event.objects.filter(is_active=True).order_by('date')
    return render(request, 'core/event_list.html', {'events': events})

@login_required
@user_passes_test(is_admin)
def post_event(request):
    """
    Admin view to post a new event or hackathon.
    """
    if request.method == "POST":
        name = request.POST.get('name')
        event_type = request.POST.get('event_type')
        description = request.POST.get('description')
        registration_link = request.POST.get('registration_link')
        date = request.POST.get('date')
        location = request.POST.get('location')
        
        Event.objects.create(
            name=name,
            event_type=event_type,
            description=description,
            registration_link=registration_link,
            date=date,
            location=location,
            posted_by=request.user
        )
        
        messages.success(request, "Event posted successfully!")
        return redirect('admin_dashboard')
        
    return render(request, 'core/post_event.html')

@login_required
@user_passes_test(is_admin)
def delete_event(request, event_id):
    event = get_object_or_404(Event, id=event_id)
    event.delete()
    messages.success(request, "Event deleted successfully.")
    return redirect('admin_dashboard')
