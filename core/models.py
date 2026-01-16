from django.db import models
from django.contrib.auth.models import User
import uuid


# Job Application / Posting Model
class JobPosting(models.Model):
    JOB_TYPES = (
        ('FULL_TIME', 'Full Time'),
        ('PART_TIME', 'Part Time'),
        ('INTERNSHIP', 'Internship'),
        ('CONTRACT', 'Contract'),
    )
    
    title = models.CharField(max_length=200)
    company_name = models.CharField(max_length=200)
    location = models.CharField(max_length=200, default="Remote")
    salary_range = models.CharField(max_length=100, blank=True, help_text="e.g. $50k - $70k or Competitive")
    job_type = models.CharField(max_length=20, choices=JOB_TYPES, default='FULL_TIME')
    description = models.TextField()
    apply_link = models.URLField(help_text="Direct link to company application page")
    posted_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)
    
    # Optional: link to author (admin)
    posted_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return f"{self.title} at {self.company_name}"

    class Meta:
        ordering = ['-posted_at']

# Events & Hackathons Model
class Event(models.Model):
    EVENT_TYPES = (
        ('HACKATHON', 'Hackathon'),
        ('WEBINAR', 'Webinar'),
        ('WORKSHOP', 'Workshop'),
        ('CONFERENCE', 'Conference'),
        ('OTHER', 'Other'),
    )
    
    name = models.CharField(max_length=200)
    event_type = models.CharField(max_length=20, choices=EVENT_TYPES, default='HACKATHON')
    description = models.TextField()
    registration_link = models.URLField(help_text="Link to register for the event")
    date = models.DateTimeField(help_text="When the event starts")
    location = models.CharField(max_length=200, default="Online", help_text="Venue or Online")
    posted_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)
    posted_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return f"{self.name} ({self.get_event_type_display()})"

    class Meta:
        ordering = ['-date']
