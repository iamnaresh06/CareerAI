from django.urls import path
from .views_resume import resume_builder, resume_download

urlpatterns = [
    path("resume/", resume_builder, name="resume_builder"),
    path("resume/download/", resume_download, name="resume_download"),
]