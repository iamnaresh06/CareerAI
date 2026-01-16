from django.shortcuts import render, redirect
from django.contrib import messages
from django.core.files.storage import FileSystemStorage
from django.conf import settings
from django.urls import reverse
from django.http import JsonResponse, FileResponse, Http404
from django.contrib.auth.decorators import login_required
import os

from core.utils import extract_resume_text, clean_text
from core.ml_engine import calculate_final_score, get_missing_skills
from core.ai_feedback import generate_feedback
from core.voice_engine import generate_voice
from core.skill_recommender import generate_skill_guidance
from core.career_chatbot import get_chatbot_response
from core.readiness_engine import calculate_job_readiness, generate_action_plan

@login_required
def dashboard(request):
    """
    User Dashboard: Central hub for the user.
    """
    return render(request, 'core/dashboard.html')

@login_required
def analyze_resume(request):
    if request.method == "POST":
        resume_file = request.FILES.get('resume')
        job_description = request.POST.get('job_description')

        if not resume_file or not job_description:
            messages.error(request, "Please upload resume and paste job description")
            return redirect('analyze')

        # save resume file
        fs = FileSystemStorage()
        filename = fs.save(resume_file.name, resume_file)
        file_path = fs.path(filename)

        # extract and clean text
        try:
            resume_text = extract_resume_text(file_path)
            job_description_cleaned = clean_text(job_description)[:3000]

            # ML scoring
            final_score, skill_score, text_score = calculate_final_score(
                resume_text,
                job_description_cleaned
            )

            missing_skills = get_missing_skills(
                resume_text,
                job_description_cleaned
            )
            skill_guidance = generate_skill_guidance(missing_skills)

            # ✅ Save data for Job Readiness feature
            request.session["last_resume_score"] = final_score
            request.session["last_skill_score"] = skill_score
            request.session["last_missing_skills"] = missing_skills
            
            feedback_message = generate_feedback(
                final_score,
                skill_score,
                missing_skills
            )

            # generate AI voice feedback
            audio_filename = generate_voice(
                feedback_message,
                settings.MEDIA_ROOT,
                request.user.username
            )

            # IMPORTANT: build browser-accessible URL
            audio_url = reverse('stream_audio', args=[audio_filename])

            context = {
                'match_score': final_score,
                'skill_score': skill_score,
                'text_score': text_score,
                'missing_skills': missing_skills,
                'feedback_message': feedback_message,
                'audio_url': audio_url,
                "skill_guidance" : skill_guidance
            }

            return render(request, 'core/analyze.html', context)
        except Exception as e:
            messages.error(request, f"Error analyzing resume: {str(e)}")
            return redirect('analyze')

    return render(request, 'core/analyze.html')

def stream_audio(request, filename):
    audio_path = os.path.join(settings.MEDIA_ROOT, filename)

    if not os.path.exists(audio_path):
        raise Http404("Audio not found")

    return FileResponse(
        open(audio_path, 'rb'),
        content_type='audio/mpeg'
    )

def career_chatbot_api(request):
    if request.method == "POST":
        message = request.POST.get("message")

        resume_score = request.session.get("last_resume_score")
        missing_skills = request.session.get("last_missing_skills")

        reply = get_chatbot_response(
            message,
            resume_score=resume_score,
            missing_skills=missing_skills
        )

        return JsonResponse({"reply": reply})
    return JsonResponse({"error": "Invalid request"}, status=400)

@login_required
def job_readiness_view(request):
    # These values already exist from analysis (safe defaults)
    resume_score = request.session.get("last_resume_score", 0)
    skill_score = request.session.get("last_skill_score", 0)
    missing_skills = request.session.get("last_missing_skills", [])

    readiness_score = calculate_job_readiness(
        resume_score,
        skill_score,
        missing_skills
    )

    action_plan = generate_action_plan(missing_skills)

    context = {
        "readiness_score": readiness_score,
        "resume_score": resume_score,
        "skill_score": skill_score,
        "action_plan": action_plan
    }

    return render(request, "core/job_readiness.html", context)
