"""
Resume Analysis Views for CareerAI.

This module handles the core resume processing logic:
1. File Upload & Parsing (PDF/DOCX).
2. ML Analysis (Scoring & Skill Extraction).
3. Feedback Generation & Audio Synthesis.
4. Job Readiness Assessment.

Author: Naresh Reddy
"""

from django.shortcuts import render, redirect
from django.contrib import messages
from django.core.files.storage import FileSystemStorage
from django.conf import settings
from django.urls import reverse
from django.http import JsonResponse, FileResponse, Http404
from django.contrib.auth.decorators import login_required
import os

# Core Logic Engines
from .file_parser import extract_resume_text, clean_text
from .ml_engine import calculate_final_score, get_missing_skills, generate_feedback_message
from .voice_engine import generate_voice
from .skill_engine import generate_skill_guidance
from .career_chatbot import get_chatbot_response
from .career_advisor import calculate_readiness_score, generate_action_plan

@login_required
def dashboard(request):
    """
    Renders the main user dashboard.
    Central hub for accessing all features (Resume Analyzer, Job Readiness, Mock Interview).
    """
    return render(request, 'core/dashboard.html')

@login_required
def analyze_resume(request):
    # ... (docstring) ...
    if request.method == "POST":
        resume_file = request.FILES.get('resume')
        job_description = request.POST.get('job_description')

        if not resume_file or not job_description:
            messages.error(request, "Please upload a resume and provide a job description.")
            return redirect('analyze')

        # Save uploaded file temporarily
        fs = FileSystemStorage()
        filename = fs.save(resume_file.name, resume_file)
        file_path = fs.path(filename)

        try:
            # Step 1: Text Extraction
            resume_text = extract_resume_text(file_path)
            # Limit JD length to avoid processing overhead
            job_description_cleaned = clean_text(job_description)[:5000]

            # Step 2: ML Analysis
            final_score, skill_score, text_score = calculate_final_score(
                resume_text,
                job_description_cleaned
            )

            missing_skills = get_missing_skills(
                resume_text,
                job_description_cleaned
            )
            
            # Step 3: Skill Guidance
            skill_guidance = generate_skill_guidance(missing_skills)

            # Step 4: Persist Data for Job Readiness Module
            request.session["last_resume_score"] = final_score
            request.session["last_skill_score"] = skill_score
            request.session["last_missing_skills"] = missing_skills
            
            # Step 5: Generate Feedback
            feedback_message = generate_feedback_message(
                final_score,
                skill_score,
                missing_skills
            )

            context = {
                'match_score': final_score,
                'skill_score': skill_score,
                'text_score': text_score,
                'missing_skills': missing_skills,
                'feedback_message': feedback_message,
                "skill_guidance" : skill_guidance
            }

            return render(request, 'core/resume_analysis/analyze.html', context)
            
        except Exception as e:
            # Helpful error logging
            print(f"Analysis Error: {e}")
            messages.error(request, f"Error analyzing resume. Please ensure the file is valid.")
            return redirect('analyze')
        finally:
            # Best practice: Clean up uploaded file
            if os.path.exists(file_path):
                os.remove(file_path)

    return render(request, 'core/resume_analysis/analyze.html')

def stream_audio(request, filename):
    # ... (same) ...
    audio_path = os.path.join(settings.MEDIA_ROOT, filename)

    if not os.path.exists(audio_path):
        raise Http404("Audio file not found")

    return FileResponse(
        open(audio_path, 'rb'),
        content_type='audio/mpeg'
    )

def career_chatbot_api(request):
    # ... (same) ...
    if request.method == "POST":
        if not request.user.is_authenticated:
            return JsonResponse({"reply": "⚠️ Please [login](/login/) or [create an account](/register/) to use the CareerAI Assistant."})
            
        message = request.POST.get("message")

        # Context-aware responses using session data
        resume_score = request.session.get("last_resume_score")
        missing_skills = request.session.get("last_missing_skills")

        reply = get_chatbot_response(
            message,
            resume_score=resume_score,
            missing_skills=missing_skills
        )

        return JsonResponse({"reply": reply})
    
    return JsonResponse({"error": "Invalid request method"}, status=405)

@login_required
def job_readiness_view(request):
    """
    Calculates and displays the user's Job Readiness Score.
    Uses data persisted from the Resume Analysis session.
    """
    # Retrieve last analysis data (default to 0 if not found)
    resume_score = request.session.get("last_resume_score", 0)
    skill_score = request.session.get("last_skill_score", 0)
    missing_skills = request.session.get("last_missing_skills", [])

    # Calculate Score
    readiness_score = calculate_readiness_score(
        resume_score,
        skill_score,
        len(missing_skills)
    )

    # Generate personalized plan
    action_plan = generate_action_plan(missing_skills)

    context = {
        "readiness_score": readiness_score,
        "resume_score": resume_score,
        "skill_score": skill_score,
        "action_plan": action_plan
    }

    return render(request, "core/resume_analysis/job_readiness.html", context)
