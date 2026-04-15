"""
URL Configuration for CareerAI.

This file maps URLs to their corresponding views, now organized by feature with specific view filenames.
"""

from django.urls import path
from django.contrib.auth import views as django_auth_views

# Feature-based View Imports
from core.authentication import auth_views
from core.jobs import job_views
from core.events import event_views
from core.resume_analysis import analysis_views
from core.resume_builder import builder_views
from core.interview import interview_views
from core.administration import admin_views

urlpatterns = [
    # -------------------------------------------------------------------------
    # Authentication & Main
    # -------------------------------------------------------------------------
    path('', auth_views.landing_page, name='home'),
    path('about/', auth_views.about_page, name='about'),
    path('register/', auth_views.register_view, name='register'),
    path('login/', auth_views.login_view, name='login'),
    path('logout/', auth_views.logout_view, name='logout'),
    path('profile/', auth_views.profile_view, name='profile'),
    path('privacy-policy/', auth_views.privacy_policy, name='privacy_policy'),
    path('terms-conditions/', auth_views.terms_conditions, name='terms_conditions'),
    path('refund-policy/', auth_views.refund_policy, name='refund_policy'),
    path('careers/', auth_views.careers_page, name='careers'),
    path('roadmaps/', auth_views.roadmaps_view, name='roadmaps'),
    
    # Dashboard (Currently hosted in analysis views)
    path('dashboard/', analysis_views.dashboard, name='dashboard'),
    path('book-service/', auth_views.book_service, name='book_service'),

    # -------------------------------------------------------------------------
    # Job Board
    # -------------------------------------------------------------------------
    path('jobs/', job_views.job_list, name='job_list'),
    path('jobs/<int:job_id>/', job_views.job_detail, name='job_detail'),
    path('jobs/post/', job_views.post_job, name='post_job'),
    path('jobs/delete/<int:job_id>/', job_views.delete_job, name='delete_job'),

    # -------------------------------------------------------------------------
    # Events & Hackathons
    # -------------------------------------------------------------------------
    path('events/', event_views.event_list, name='event_list'),
    path('events/post/', event_views.post_event, name='post_event'),
    path('events/delete/<int:event_id>/', event_views.delete_event, name='delete_event'),

    # -------------------------------------------------------------------------
    # Administration
    # -------------------------------------------------------------------------
    path('admin-dashboard/', admin_views.admin_dashboard, name='admin_dashboard'),
    path('admin-dashboard/user/<int:user_id>/', admin_views.admin_user_profile, name='admin_user_profile'),
    path('admin-dashboard/booking/<int:booking_id>/update/', admin_views.update_booking_status, name='update_booking_status'),
    
    # -------------------------------------------------------------------------
    # Resume Analysis & AI Tools
    # -------------------------------------------------------------------------
    path('analyze/', analysis_views.analyze_resume, name='analyze'),
    path('audio/<str:filename>/', analysis_views.stream_audio, name='stream_audio'),
    path("career-chatbot/", analysis_views.career_chatbot_api, name="career_chatbot"),
    path("job-readiness/", analysis_views.job_readiness_view, name="job_readiness"),
    
    # -------------------------------------------------------------------------
    # Resume Builder
    # -------------------------------------------------------------------------
    path("resume-builder/", builder_views.resume_builder, name="resume_builder"),
    path("resume-parse/", builder_views.resume_parse, name="resume_parse"),
    path("resume-save/", builder_views.resume_save, name="resume_save"),
    path("resume-preview/", builder_views.resume_preview, name="resume_preview"),
    path("resume-download/", builder_views.resume_download, name="resume_download"),
    path("resume-edit/", builder_views.resume_edit, name="resume_edit"),
    
    # -------------------------------------------------------------------------
    # AI Mock Interview
    # -------------------------------------------------------------------------
    path("interview/", interview_views.interview_hub, name="interview_hub"),
    path("interview/<str:category>/", interview_views.start_interview, name="start_interview"),
    path("api/interview/analyze/", interview_views.process_answer, name="process_answer"),

    # -------------------------------------------------------------------------
    # Password Reset (Standard Django Views)
    # -------------------------------------------------------------------------
    path("forgot-password/", django_auth_views.PasswordResetView.as_view(template_name="core/authentication/password_reset.html"), name="password_reset"),
    path("forgot-password/done/", django_auth_views.PasswordResetDoneView.as_view(template_name="core/authentication/password_reset_done.html"), name="password_reset_done"),
    path("reset/<uidb64>/<token>/", django_auth_views.PasswordResetConfirmView.as_view(template_name="core/authentication/password_reset_confirm.html"), name="password_reset_confirm"),
    path("reset/done/", django_auth_views.PasswordResetCompleteView.as_view(template_name="core/authentication/password_reset_complete.html"), name="password_reset_complete"),
]