from django.urls import path
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