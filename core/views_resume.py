from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.template.loader import render_to_string
from xhtml2pdf import pisa
import io
from datetime import datetime


# ==============================
# HELPERS
# ==============================

def categorize_skills(skills_string):
    skills = [s.strip() for s in skills_string.split(",") if s.strip()]

    programming, web, core, tools = [], [], [], []

    for skill in skills:
        s = skill.lower()

        if s in ["python", "java", "c", "c++", "javascript"]:
            programming.append(skill)
        elif s in ["html", "css", "django", "react", "angular", "vue", "flask"]:
            web.append(skill)
        elif s in ["data structures", "dsa", "algorithms", "computer networks", "dbms", "os"]:
            core.append(skill)
        else:
            tools.append(skill)

    return {
        "programming": programming,
        "web": web,
        "core": core,
        "tools": tools,
    }


def text_to_bullets(text):
    if not text:
        return []
    return [line.strip() for line in text.split("\n") if line.strip()]


def shorten_summary(text, limit=400):
    if not text:
        return ""
    if len(text) <= limit:
        return text
    return text[:limit].rsplit(" ", 1)[0] + "..."


def format_month_year(value):
    try:
        return datetime.strptime(value, "%Y-%m").strftime("%b %Y")
    except:
        return value


# ==============================
# VIEWS
# ==============================

def resume_builder(request):
    """
    Resume form page.
    If user is editing, data is loaded from session.
    """
    data = request.session.get("resume_data", {})
    return render(request, "resume/resume_builder.html", data)


def resume_save(request):
    """
    Handles BOTH:
    - Preview
    - Download
    Stores data in session (single source of truth)
    """
    if request.method != "POST":
        return redirect("resume_builder")

    # ---------- EDUCATION ----------
    education = []
    edu_degrees = request.POST.getlist("edu_degree[]")
    edu_colleges = request.POST.getlist("edu_college[]")
    edu_starts = request.POST.getlist("edu_start[]")
    edu_ends = request.POST.getlist("edu_end[]")

    for i in range(len(edu_degrees)):
        end_raw = edu_ends[i] if i < len(edu_ends) else ""
        end = format_month_year(end_raw) if end_raw else "Present"

        education.append({
            "degree": edu_degrees[i],
            "college": edu_colleges[i],
            "start": format_month_year(edu_starts[i]),
            "end": end,
            "score": request.POST.getlist("edu_score[]")[i],
        })

    # ---------- EXPERIENCE ----------
    experience = []
    exp_roles = request.POST.getlist("exp_role[]")
    exp_companies = request.POST.getlist("exp_company[]")
    exp_starts = request.POST.getlist("exp_start[]")
    exp_ends = request.POST.getlist("exp_end[]")
    exp_descs = request.POST.getlist("exp_desc[]")

    for i in range(len(exp_roles)):
        end_raw = exp_ends[i] if i < len(exp_ends) else ""
        end = format_month_year(end_raw) if end_raw else "Present"

        experience.append({
            "role": exp_roles[i],
            "company": exp_companies[i],
            "start": format_month_year(exp_starts[i]),
            "end": end,
            "desc": text_to_bullets(exp_descs[i])[:3],
        })


    # ---------- PROJECTS ----------
    projects = []
    for i in range(len(request.POST.getlist("proj_name[]"))):
        projects.append({
            "name": request.POST.getlist("proj_name[]")[i],
            "stack": request.POST.getlist("proj_stack[]")[i],
            "desc": text_to_bullets(request.POST.getlist("proj_desc[]")[i])[:3],
        })

    # ---------- CERTIFICATIONS ----------
    certifications = []
    for i in range(len(request.POST.getlist("cert_name[]"))):
        certifications.append({
            "name": request.POST.getlist("cert_name[]")[i],
            "org": request.POST.getlist("cert_org[]")[i],
        })

    # ---------- FINAL CONTEXT ----------
    context = {
        "full_name": request.POST.get("full_name"),
        "email": request.POST.get("email"),
        "phone": request.POST.get("phone"),
        "linkedin": request.POST.get("linkedin"),
        "github": request.POST.get("github"),
        "portfolio": request.POST.get("portfolio"),
        "summary": shorten_summary(request.POST.get("summary", "")),
        "skills": categorize_skills(request.POST.get("skills", "")),
        "show_skill_categories": request.POST.get("show_skill_categories") == "on",
        "education": education,
        "experience": experience,
        "projects": projects,
        "certifications": certifications,
    }

    # ✅ SAVE ONCE — USED EVERYWHERE
    request.session["resume_data"] = context

    # ---------- ACTION ----------
    if request.POST.get("action") == "preview":
        return redirect("resume_preview")

    return redirect("resume_download")


def resume_preview(request):
    """
    Clean HTML preview (no gradients, no base.html)
    """
    data = request.session.get("resume_data")
    if not data:
        return redirect("resume_builder")

    return render(request, "resume/resume_preview.html", data)


def resume_download(request):
    """
    Generate PDF from session data
    """
    data = request.session.get("resume_data")
    if not data:
        return redirect("resume_builder")

    html = render_to_string("resume/resume_pdf.html", data)

    response = HttpResponse(content_type="application/pdf")
    response["Content-Disposition"] = "attachment; filename=ATS_Resume.pdf"

    pisa.CreatePDF(io.BytesIO(html.encode("UTF-8")), response)
    return response


def resume_edit(request):
    """
    Edit resume without losing data
    """
    return redirect("resume_builder")