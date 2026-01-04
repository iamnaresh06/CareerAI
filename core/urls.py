from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('analyze/', views.analyze_resume, name='analyze'),
    path('audio/<str:filename>/', views.stream_audio, name='stream_audio'),
    path("career-chatbot/", views.career_chatbot_api, name="career_chatbot"),
    path("job-readiness/", views.job_readiness_view, name="job_readiness"),
]




urlpatterns += [

    path(
        "forgot-password/",
        auth_views.PasswordResetView.as_view(
            template_name="core/password_reset.html"
        ),
        name="password_reset",
    ),

    path(
        "forgot-password/done/",
        auth_views.PasswordResetDoneView.as_view(
            template_name="core/password_reset_done.html"
        ),
        name="password_reset_done",
    ),

    path(
        "reset/<uidb64>/<token>/",
        auth_views.PasswordResetConfirmView.as_view(
            template_name="core/password_reset_confirm.html"
        ),
        name="password_reset_confirm",
    ),

    path(
        "reset/done/",
        auth_views.PasswordResetCompleteView.as_view(
            template_name="core/password_reset_complete.html"
        ),
        name="password_reset_complete",
    ),
]