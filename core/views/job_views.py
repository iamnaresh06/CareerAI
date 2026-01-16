from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from core.models import JobPosting

# Helper to check if user is admin
def is_admin(user):
    return user.is_superuser or user.is_staff

@login_required
def job_list(request):
    """
    Displays a list of all active job and internship postings.
    Allows filtering by type via query parameter 'type'.
    """
    filter_type = request.GET.get('type') # e.g., 'INTERNSHIP' or 'FULL_TIME'
    
    jobs = JobPosting.objects.filter(is_active=True)
    
    if filter_type:
        jobs = jobs.filter(job_type=filter_type)
        
    context = {
        'jobs': jobs,
        'filter_type': filter_type
    }
    return render(request, 'core/job_list.html', context)

@login_required
def job_detail(request, job_id):
    job = get_object_or_404(JobPosting, id=job_id)
    return render(request, 'core/job_detail.html', {'job': job})

@login_required
@user_passes_test(is_admin)
def post_job(request):
    """
    Admin view to post a new job or internship.
    """
    if request.method == "POST":
        title = request.POST.get('title')
        company_name = request.POST.get('company_name')
        location = request.POST.get('location')
        salary_range = request.POST.get('salary_range')
        job_type = request.POST.get('job_type')
        description = request.POST.get('description')
        apply_link = request.POST.get('apply_link')
        
        JobPosting.objects.create(
            title=title,
            company_name=company_name,
            location=location,
            salary_range=salary_range,
            job_type=job_type,
            description=description,
            apply_link=apply_link,
            posted_by=request.user
        )
        
        messages.success(request, "Job posted successfully!")
        return redirect('admin_dashboard')
        
    return render(request, 'core/post_job.html')

@login_required
@user_passes_test(is_admin)
def delete_job(request, job_id):
    job = get_object_or_404(JobPosting, id=job_id)
    job.delete()
    messages.success(request, "Job deleted successfully.")
    return redirect('admin_dashboard')
