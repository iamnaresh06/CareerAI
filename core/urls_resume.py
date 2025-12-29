from django.urls import path
from .views_resume import (
    resume_builder,
    resume_save,
    resume_preview,
    resume_download,
    resume_edit,
)

urlpatterns = [
    # Resume Builder (Create / Edit)
    path("resume/", resume_builder, name="resume_builder"),

    # Save resume data (handles Preview & Download action)
    path("resume/save/", resume_save, name="resume_save"),

    # Preview resume (HTML preview, clean layout)
    path("resume/preview/", resume_preview, name="resume_preview"),

    # Download resume as PDF (uses session data)
    path("resume/download/", resume_download, name="resume_download"),

    # Edit resume (redirects back to builder with data)
    path("resume/edit/", resume_edit, name="resume_edit"),
]
