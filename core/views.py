
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout

from django.shortcuts import render, redirect
from django.contrib import messages
from django.core.files.storage import FileSystemStorage

from .utils import extract_resume_text, clean_text
from .ml_engine import (
    calculate_final_score,
    get_missing_skills
)
from .ai_feedback import generate_feedback
from django.conf import settings
from .voice_engine import generate_voice
from django.urls import reverse
import os
from .skill_recommender import generate_skill_guidance



def home(request):
    return redirect('login')

def register_view(request):
    if request.method == "POST":
        first_name = request.POST.get("first_name")
        last_name = request.POST.get("last_name")
        email = request.POST.get("email")
        username = request.POST.get("username")
        password = request.POST.get("password")
        confirm_password = request.POST.get("confirm_password")

        if password != confirm_password:
            messages.error(request, "Passwords do not match")
            return redirect("register")

        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists")
            return redirect("register")

        if User.objects.filter(email=email).exists():
            messages.error(request, "Email already registered")
            return redirect("register")

        user = User.objects.create_user(
            username=username,
            email=email,
            password=password,
            first_name=first_name,
            last_name=last_name
        )

        messages.success(request, "Account created successfully")
        return redirect("login")

    return render(request, "core/register.html")


def login_view(request):
    # Handle user login
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('dashboard')
        else:
            messages.error(request, "Invalid username or password")
            return redirect('login')

    return render(request, 'core/login.html')


def logout_view(request):
    logout(request)
    return redirect('login')


def dashboard(request):
    # simple protected page
    if not request.user.is_authenticated:
        return redirect('login')

    return render(request, 'core/dashboard.html')




def analyze_resume(request):
    if not request.user.is_authenticated:
        return redirect('login')

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

    return render(request, 'core/analyze.html')



from django.http import FileResponse, Http404

def stream_audio(request, filename):
    audio_path = os.path.join(settings.MEDIA_ROOT, filename)

    if not os.path.exists(audio_path):
        raise Http404("Audio not found")

    return FileResponse(
        open(audio_path, 'rb'),
        content_type='audio/mpeg'
    )


from django.http import JsonResponse
from .career_chatbot import get_chatbot_response

def career_chatbot_api(request):
    if request.method == "POST":
        message = request.POST.get("message")

        # optional context
        resume_score = request.session.get("last_score")
        missing_skills = request.session.get("last_missing_skills")

        reply = get_chatbot_response(
            message,
            resume_score=resume_score,
            missing_skills=missing_skills
        )

        return JsonResponse({"reply": reply})
    




from .readiness_engine import calculate_job_readiness, generate_action_plan

def job_readiness_view(request):
    if not request.user.is_authenticated:
        return redirect("login")

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