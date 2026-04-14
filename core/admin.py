from django.contrib import admin
from .models import JobPosting, Event, UserProfile, ServiceBooking

@admin.register(ServiceBooking)
class ServiceBookingAdmin(admin.ModelAdmin):
    list_display = ('user', 'service_type', 'phone_number', 'status', 'created_at')
    list_filter = ('status', 'service_type')
    search_fields = ('user__username', 'phone_number', 'preferred_tech')

@admin.register(JobPosting)
class JobPostingAdmin(admin.ModelAdmin):
    list_display = ('title', 'company_name', 'job_type', 'posted_at', 'is_active')
    list_filter = ('is_active', 'job_type')

@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ('name', 'event_type', 'date', 'is_active')
    list_filter = ('is_active', 'event_type')

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'student_id', 'contact_number')
