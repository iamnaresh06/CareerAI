from django.shortcuts import render
from django.http import HttpResponse
from django.template.loader import render_to_string
from xhtml2pdf import pisa
import io



def categorize_skills(skills_string):
    skills = [s.strip() for s in skills_string.split(",") if s.strip()]

    programming = []
    web = []
    core = []
    tools = []

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
        "tools": tools
    }


def text_to_bullets(text):
    if not text:
        return []
    return [line.strip() for line in text.split("\n") if line.strip()]



def shorten_summary(text, limit=350):
    if not text:
        return ""
    return text[:limit].rsplit(" ", 1)[0] + "..."


from datetime import datetime

def format_month_year(value):
    try:
        return datetime.strptime(value, "%Y-%m").strftime("%b %Y")
    except:
        return value



def resume_builder(request):
    return render(request, "resume/resume_builder.html")

def resume_download(request):
    if request.method != "POST":
        return HttpResponse("Invalid request")

    education = []
    for i in range(len(request.POST.getlist("edu_degree[]"))):
        education.append({
            "degree": request.POST.getlist("edu_degree[]")[i],
            "college": request.POST.getlist("edu_college[]")[i],
            "start": format_month_year(request.POST.getlist("edu_start[]")[i]),
            "end": format_month_year(request.POST.getlist("edu_end[]")[i]),
            "score": request.POST.getlist("edu_score[]")[i],
        })

    experience = []
    for i in range(len(request.POST.getlist("exp_role[]"))):
        experience.append({
            "role": request.POST.getlist("exp_role[]")[i],
            "company": request.POST.getlist("exp_company[]")[i],
            "start": format_month_year(request.POST.getlist("exp_start[]")[i]),
            "end": format_month_year(request.POST.getlist("exp_end[]")[i]),
            "desc": text_to_bullets(request.POST.getlist("exp_desc[]")[i]),
        })

    projects = []
    for i in range(len(request.POST.getlist("proj_name[]"))):
        projects.append({
            "name": request.POST.getlist("proj_name[]")[i],
            "stack": request.POST.getlist("proj_stack[]")[i],
            "desc": text_to_bullets(request.POST.getlist("proj_desc[]")[i]),
        })

    certifications = []
    for i in range(len(request.POST.getlist("cert_name[]"))):
        certifications.append({
            "name": request.POST.getlist("cert_name[]")[i],
            "org": request.POST.getlist("cert_org[]")[i],
        })

    context = {
        "full_name": request.POST.get("full_name"),
        "email": request.POST.get("email"),
        "phone": request.POST.get("phone"),
        "linkedin": request.POST.get("linkedin"),
        "github": request.POST.get("github"),
        "summary": shorten_summary(request.POST.get("summary", "")),
        "skills": categorize_skills(request.POST.get("skills", "")),
        "show_skill_categories": request.POST.get("show_skill_categories") == "on",
        "education": education,
        "experience": experience,
        "projects": projects,
        "certifications": certifications,
    }

    html = render_to_string("resume/resume_pdf.html", context)

    response = HttpResponse(content_type="application/pdf")
    response["Content-Disposition"] = "attachment; filename=ATS_Resume.pdf"

    pisa.CreatePDF(io.BytesIO(html.encode("UTF-8")), response)
    return response