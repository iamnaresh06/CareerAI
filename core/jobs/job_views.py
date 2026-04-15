"""
Job Views for CareerAI.

This module manages the Job Board functionality, including:
1. Listing Active Jobs (Filtering by Internship/Full-time).
2. Viewing Job Details.
3. Admin Actions: Posting and Deleting Jobs.

Author: Naresh Reddy
"""

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from core.models import JobPosting
from django.utils import timezone
from django.db.models import Q

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
def job_list(request):
    """
    Displays the Job Board.
    
    Features:
    - Lists all active job postings.
    - Supports filtering by job type (Internship vs. Full-time).
    """
    filter_type = request.GET.get('type') # e.g., 'INTERNSHIP' or 'FULL_TIME'
    
    # Fetch only active and non-expired jobs (or jobs with no expiration)
    now = timezone.now()
    jobs = JobPosting.objects.filter(
        is_active=True
    ).filter(
        Q(expires_at__isnull=True) | Q(expires_at__gte=now)
    ).order_by('-posted_at')
    
    if filter_type:
        jobs = jobs.filter(job_type=filter_type)
        
    context = {
        'jobs': jobs,
        'filter_type': filter_type
    }
    return render(request, 'core/jobs/job_list.html', context)


@login_required
def job_detail(request, job_id):
    """
    Displays detailed information for a single job posting.
    """
    job = get_object_or_404(JobPosting, id=job_id)
    return render(request, 'core/jobs/job_detail.html', {'job': job})


@login_required
@user_passes_test(is_admin)
def post_job(request):
    """
    Admin View: Create a new Job Posting.
    
    1. Collects job details from the form.
    2. Suggests sensible defaults.
    3. Saves the job to the database linked to the admin user.
    """
    if request.method == "POST":
        try:
            # Extract form data
            new_job = JobPosting.objects.create(
                title=request.POST.get('title'),
                company_name=request.POST.get('company_name'),
                location=request.POST.get('location'),
                salary_range=request.POST.get('salary_range'),
                job_type=request.POST.get('job_type'),
                description=request.POST.get('description'),
                apply_link=request.POST.get('apply_link'),
                expires_at=request.POST.get('expires_at') if request.POST.get('expires_at') else None,
                posted_by=request.user
            )
            
            messages.success(request, f"New job '{new_job.title}' posted successfully!")
            return redirect('admin_dashboard')
            
        except Exception as e:
            messages.error(request, f"Error posting job: {e}")
            return redirect('post_job')
        
    return render(request, 'core/jobs/post_job.html')


@login_required
@user_passes_test(is_admin)
def delete_job(request, job_id):
    """
    Admin View: Delete a Job Posting.
    """
    job = get_object_or_404(JobPosting, id=job_id)
    
    if request.method == "POST":
        job.delete()
        messages.success(request, "Job deleted successfully.")
        
    return redirect('admin_dashboard')
