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


def generate_student_id():
    """Generates a unique student ID in the format CAI-XXXXXX"""
    import random
    import string
    chars = string.ascii_uppercase + string.digits
    while True:
        new_id = 'CAI-' + ''.join(random.choices(chars, k=6))
        if not UserProfile.objects.filter(student_id=new_id).exists():
            return new_id

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_image = models.ImageField(upload_to='profile_images/', null=True, blank=True)
    student_id = models.CharField(max_length=20, unique=True, null=True, blank=True)
    resume = models.FileField(upload_to='resumes/', null=True, blank=True)
    contact_number = models.CharField(max_length=15, null=True, blank=True)

    def __str__(self):
        return f"{self.user.username}'s Profile ({self.student_id or 'No ID'})"

# -----------------------------------------------------------------------------
# Signals
# -----------------------------------------------------------------------------
from django.db.models.signals import post_save
from django.dispatch import receiver

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(
            user=instance,
            student_id=generate_student_id()
        )

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    # Use hasattr to prevent errors if profile was somehow not created
    if hasattr(instance, 'userprofile'):
        if not instance.userprofile.student_id:
            instance.userprofile.student_id = generate_student_id()
        instance.userprofile.save()
    else:
        UserProfile.objects.create(
            user=instance,
            student_id=generate_student_id()
        )
