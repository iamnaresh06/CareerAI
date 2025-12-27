
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



def home(request):
    return redirect('login')

def register_view(request):
    # Handle user registration
    if request.method == "POST":
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        username = request.POST.get('username')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')

        # basic validations
        if password != confirm_password:
            messages.error(request, "Passwords do not match")
            return redirect('register')

        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists")
            return redirect('register')

        # create user
        user = User.objects.create_user(
            username=username,
            password=password,
            first_name=first_name,
            last_name=last_name
        )
        user.save()

        messages.success(request, "Account created successfully")
        return redirect('login')

    return render(request, 'core/register.html')


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

        feedback_message = generate_feedback(
            final_score,
            skill_score,
            missing_skills
        )

        audio_filename = generate_voice(
            feedback_message,
            settings.MEDIA_ROOT,
            request.user.username
        )



        context = {
            'match_score': final_score,
            'skill_score': skill_score,
            'text_score': text_score,
            'missing_skills': missing_skills,
            'feedback_message': feedback_message,
            'audio_file': audio_filename,
            'MEDIA_URL': settings.MEDIA_URL
        }

        return render(request, 'core/analyze.html', context)

    return render(request, 'core/analyze.html')


