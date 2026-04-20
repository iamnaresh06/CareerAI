"""
Resume Builder Views for CareerAI.

This module handles the manual resume creation process:
1. Collecting user input for education, experience, skills, etc.
2. Storing data in session.
3. Generating a preview.
4. Generating the final PDF using the Resume Generator engine.

Author: Naresh Reddy
"""

from django.shortcuts import render, redirect
from django.template.loader import render_to_string
from django.core.files.storage import FileSystemStorage
from django.contrib import messages
from datetime import datetime
import re
import os
from .generator import render_resume_pdf
from core.resume_analysis.file_parser import extract_text_from_pdf, extract_text_from_docx
from core.resume_analysis.ml_engine import extract_skills

# ==============================
# HELPERS
# ==============================

def categorize_skills(skills_string):
    """
    Parses a comma-separated string of skills and organizes them into categories.
    """
    if not skills_string:
        return {}

    skills = [s.strip() for s in skills_string.split(",") if s.strip()]

    categories = {
        "Programming Languages": [],
        "Web Technologies": [],
        "Databases": [],
        "AI & Machine Learning": [],
        "Core CS": [],
        "Tools & Platforms": [],
        "Other Skills": []
    }

    for skill in skills:
        s = skill.lower()

        if s in ["python", "java", "c", "c++", "c#", "javascript", "typescript", "go", "ruby", "php", "r", "swift", "kotlin", "rust"]:
            categories["Programming Languages"].append(skill)
        elif s in ["html", "css", "django", "react", "angular", "vue", "flask", "node", "next.js", "bootstrap", "tailwind css", "spring", "express.js", "jquery"]:
            categories["Web Technologies"].append(skill)
        elif s in ["sql", "mysql", "postgresql", "sqlite", "mongodb", "oracle", "mariadb", "redis", "firebase", "dynamodb"]:
            categories["Databases"].append(skill)
        elif s in ["machine learning", "deep learning", "nlp", "computer vision", "tensorflow", "pytorch", "keras", "scikit-learn", "numpy", "pandas", "data analysis"]:
            categories["AI & Machine Learning"].append(skill)
        elif s in ["data structures", "dsa", "algorithms", "computer networks", "dbms", "os", "system design", "oops"]:
            categories["Core CS"].append(skill)
        elif s in ["git", "github", "gitlab", "docker", "kubernetes", "aws", "azure", "gcp", "render", "heroku", "jenkins", "linux", "bash", "postman", "jira"]:
            categories["Tools & Platforms"].append(skill)
        else:
            categories["Other Skills"].append(skill)

    # Remove empty categories to keep the PDF clean
    return {k: v for k, v in categories.items() if v}


def text_to_bullets(text):
    """
    Converts newline-separated text into a list of bullet points.
    """
    if not text:
        return []
    return [line.strip() for line in text.split("\n") if line.strip()]


def shorten_summary(text, limit=400):
    """
    Truncates summary text to a specified limit, respecting word boundaries.
    """
    if not text:
        return ""
    if len(text) <= limit:
        return text
    return text[:limit].rsplit(" ", 1)[0] + "..."


def format_month_year(value):
    """
    Formats 'YYYY-MM' string to 'Mon YYYY'.
    """
    try:
        return datetime.strptime(value, "%Y-%m").strftime("%b %Y")
    except (ValueError, TypeError):
        return value


# ==============================
# VIEWS
# ==============================

def resume_builder(request):
    """
    Renders the Resume Builder form.
    Pre-fills the form if data exists in the session (allows editing).
    """
    data = request.session.get("resume_data", {})
    return render(request, "core/resume_builder/resume_builder.html", data)

def resume_parse(request):
    """
    Handles file upload, parses resume, extracts known fields, and populates the builder session.
    """
    if request.method == "POST" and request.FILES.get("resume_file"):
        resume_file = request.FILES["resume_file"]
        fs = FileSystemStorage()
        filename = fs.save(resume_file.name, resume_file)
        file_path = fs.path(filename)
        
        try:
            # Determine format and extract text
            ext = os.path.splitext(filename)[1].lower()
            text = ""
            if ext == '.pdf':
                text = extract_text_from_pdf(file_path)
            elif ext == '.docx':
                text = extract_text_from_docx(file_path)
            
            if not text:
                messages.error(request, "Could not extract text from the uploaded file.")
                return redirect("resume_builder")
                
            # Extract basic information using regex
            # Email
            email_match = re.search(r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}', text)
            email = email_match.group(0) if email_match else ""
            
            # Phone (basic formats)
            phone_match = re.search(r'\+?\d{1,3}?[-.\s]?\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}', text)
            phone = phone_match.group(0) if phone_match else ""
            
            # LinkedIn
            linkedin_match = re.search(r'(https?://(?:www\.)?linkedin\.com/in/[a-zA-Z0-9_-]+)', text)
            linkedin = linkedin_match.group(1) if linkedin_match else ""
            
            # GitHub
            github_match = re.search(r'(https?://(?:www\.)?github\.com/[a-zA-Z0-9_-]+)', text)
            github = github_match.group(1) if github_match else ""
            
            # Name heuristic: take the first non-empty line as name (often works for resumes)
            lines = [line.strip() for line in text.split('\n') if line.strip()]
            full_name = lines[0] if lines else ""
            
            # Skills extraction
            skills_list = extract_skills(text)
            skills_str = ", ".join(skills_list)
            
            # --- STRUCTURED DATA HEURISTICS ---
            # --- STRUCTURED DATA HEURISTICS ---
            section_headers = {
                "education": ["EDUCATION", "ACADEMIC BACKGROUND", "ACADEMICS"],
                "experience": ["EXPERIENCE", "WORK EXPERIENCE", "EMPLOYMENT HISTORY", "PROFESSIONAL EXPERIENCE", "INTERNSHIP EXPERIENCE"],
                "projects": ["PROJECTS", "PERSONAL PROJECTS", "ACADEMIC PROJECTS"],
                "certifications": ["CERTIFICATIONS", "CERTIFICATES", "LICENSES"],
                "ignore": ["SKILLS & TECHNOLOGIES", "SKILLS", "TECHNOLOGIES", "SUMMARY", "PROFESSIONAL SUMMARY", "PROFILE", "LANGUAGES", "ACHIEVEMENTS", "INTERESTS"]
            }

            blocks = {"education": [], "experience": [], "projects": [], "certifications": [], "ignore": []}
            current_sec = "ignore"
            
            raw_lines = [line.strip() for line in text.split('\n')]
            
            for line in raw_lines:
                if not line: continue
                # Check if line is a header
                upper_line = line.upper().strip()
                clean_header = re.sub(r'[^A-Z\s]', '', upper_line).strip()
                matched = False
                for sec_key, keywords in section_headers.items():
                    if clean_header in keywords or any(clean_header == k for k in keywords):
                        current_sec = sec_key
                        matched = True
                        break
                if not matched:
                    blocks[current_sec].append(line)

            def get_date_range(block_text):
                match = re.search(r'((?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)[a-z]*\.?\s*\d{4}|\d{4})\s*[-–to]{1,3}\s*((?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)[a-z]*\.?\s*\d{4}|\d{4}|Present|Current)', block_text, re.IGNORECASE)
                if match:
                    return match.group(1), match.group(2).title()
                match = re.search(r'\b([12][0-9]{3})\b', block_text)
                return (match.group(1), '') if match else ('', '')
                
            def reformat_date(date_str):
                if not date_str or date_str.lower() in ['present', 'current']:
                    return "Present" if date_str.lower() in ['present', 'current'] else ""
                try:
                    match = re.search(r'(Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)[a-z]*\.?\s*([12][0-9]{3})', date_str, re.IGNORECASE)
                    if match:
                        month_str = match.group(1)[:3].title()
                        months = {"Jan":"01", "Feb":"02", "Mar":"03", "Apr":"04", "May":"05", "Jun":"06", "Jul":"07", "Aug":"08", "Sep":"09", "Oct":"10", "Nov":"11", "Dec":"12"}
                        return f"{match.group(2)}-{months[month_str]}"
                    match_year = re.search(r'([12][0-9]{3})', date_str)
                    if match_year: return f"{match_year.group(1)}-01"
                except: pass
                return ""

            education = []
            edu_lines = blocks["education"]
            i = 0
            while i < len(edu_lines) and len(education) < 2:
                line = edu_lines[i]
                start_raw, end_raw = get_date_range(line)
                degree = line.split('|')[0].strip() if '|' in line else line
                
                college, score = "", ""
                if i + 1 < len(edu_lines):
                    college_line = edu_lines[i+1]
                    college = college_line.split('–')[0].strip() if '–' in college_line else college_line
                    if not start_raw: 
                        start_raw, end_raw = get_date_range(college_line)
                if i + 2 < len(edu_lines) and any(kw in edu_lines[i+2] for kw in ['CGPA', 'GPA', '%', 'Percentage']):
                    score = re.sub(r'[^0-9.]', '', edu_lines[i+2]).strip()
                    i += 3
                else:
                    i += 2
                
                education.append({
                    "degree": re.sub(r'\|.*', '', degree).strip()[:100], 
                    "college": re.sub(r'\|.*', '', college).strip()[:100],
                    "start": reformat_date(start_raw), 
                    "start_display": start_raw,
                    "end": reformat_date(end_raw), 
                    "end_display": end_raw,
                    "score": score[:20]
                })

            experience = []
            exp_lines = blocks["experience"]
            curr_exp = None
            for line in exp_lines:
                date_check = get_date_range(line)
                if '|' in line or '–' in line or date_check[0] != '':
                    if curr_exp: experience.append(curr_exp)
                    start_raw, end_raw = date_check
                    parts = [p.strip() for p in re.split(r'\||–', line)]
                    role = parts[0]
                    company = parts[1] if len(parts) > 1 else ""
                    company = re.sub(r'((?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)[a-z]*\.?\s*\d{4}|\d{4}).*', '', company).strip()
                    curr_exp = {
                        "role": role[:100], "company": company[:100], 
                        "start": reformat_date(start_raw), "start_display": start_raw,
                        "end": reformat_date(end_raw), "end_display": end_raw,
                        "desc": []
                    }
                else:
                    if curr_exp and len(curr_exp["desc"]) < 3:
                        clean_desc = line.lstrip('•-* ').strip()
                        if clean_desc: curr_exp["desc"].append(clean_desc)
            if curr_exp: experience.append(curr_exp)
            experience = experience[:2]

            projects = []
            proj_lines = blocks["projects"]
            curr_proj = None
            for line in proj_lines:
                if '|' in line or re.match(r'^\d+\.', line):
                    if curr_proj: projects.append(curr_proj)
                    clean_name = re.sub(r'^\d+\.\s*', '', line) 
                    parts = [p.strip() for p in clean_name.split('|')]
                    name = parts[0].split('–')[0].strip() if '–' in parts[0] else parts[0]
                    stack = parts[1] if len(parts) > 1 else ""
                    curr_proj = {"name": name[:100], "stack": stack[:100], "desc": []}
                else:
                    if curr_proj and len(curr_proj["desc"]) < 3:
                        clean_desc = line.lstrip('•-* ').strip()
                        if clean_desc: curr_proj["desc"].append(clean_desc)
            if curr_proj: projects.append(curr_proj)
            projects = projects[:2]

            certifications = []
            for line in blocks["certifications"]:
                clean_line = line.lstrip('•-* 1234567890.').strip()
                if not clean_line: continue
                parts = re.split(r'\s*[-–|,]\s*', clean_line, maxsplit=1)
                name = parts[0][:100]
                org = parts[1][:100] if len(parts) > 1 else ""
                certifications.append({"name": name, "org": org})
                if len(certifications) >= 2: break

            # Update session with parsed fields, preserving other fields if already present
            data = request.session.get("resume_data", {})
            data['full_name'] = data.get('full_name') or full_name
            data['email'] = data.get('email') or email
            data['phone'] = data.get('phone') or phone
            data['linkedin'] = data.get('linkedin') or linkedin
            data['github'] = data.get('github') or github
            data['skills_raw'] = data.get('skills_raw') or skills_str
            
            # For arrays, overwrite them with AI parsed data if we found any sections
            if education: data['education'] = education
            if experience: data['experience'] = experience
            if projects: data['projects'] = projects
            if certifications: data['certifications'] = certifications
            
            request.session["resume_data"] = data
            messages.success(request, "Resume parsed successfully! Please review the extracted fields.")
            
        except Exception as e:
            messages.error(request, f"Error parsing resume: {str(e)}")
        finally:
            # Clean up the uploaded file
            if fs.exists(filename):
                fs.delete(filename)
                
    return redirect("resume_builder")


def resume_save(request):
    """
    Processes the Resume Builder form submission.
    
    1. Extracts lists of data (Education, Experience, Projects).
    2. Formats dates and descriptions.
    3. Categorizes skills.
    4. Saves everything to the session.
    5. Redirects to Preview or Download based on user action.
    """
    if request.method != "POST":
        return redirect("resume_builder")

    # Helper to safely get lists from POST data
    def get_list(key):
        return request.POST.getlist(key)

    # ---------- EDUCATION ----------
    education = []
    edu_degrees = get_list("edu_degree[]")
    edu_colleges = get_list("edu_college[]")
    edu_starts = get_list("edu_start[]")
    edu_ends = get_list("edu_end[]")
    edu_scores = get_list("edu_score[]")

    for i in range(len(edu_degrees)):
        # Ensure we don't index out of bounds if lists are uneven
        if i >= len(edu_degrees): break
        
        start_val = edu_starts[i]
        end_raw = edu_ends[i] if i < len(edu_ends) else ""
        end_val = end_raw if end_raw else "Present"
        score = edu_scores[i] if i < len(edu_scores) else ""

        education.append({
            "degree": edu_degrees[i],
            "college": edu_colleges[i],
            "start": start_val,
            "start_display": format_month_year(start_val),
            "end": end_val,
            "end_display": format_month_year(end_val) if end_val != "Present" else "Present",
            "score": score,
        })

    # ---------- EXPERIENCE ----------
    experience = []
    exp_roles = get_list("exp_role[]")
    exp_companies = get_list("exp_company[]")
    exp_starts = get_list("exp_start[]")
    exp_ends = get_list("exp_end[]")
    exp_descs = get_list("exp_desc[]")

    for i in range(len(exp_roles)):
        if i >= len(exp_roles): break
        
        start_val = exp_starts[i]
        end_raw = exp_ends[i] if i < len(exp_ends) else ""
        end_val = end_raw if end_raw else "Present"
        desc_list = text_to_bullets(exp_descs[i]) if i < len(exp_descs) else []

        experience.append({
            "role": exp_roles[i],
            "company": exp_companies[i],
            "start": start_val,
            "start_display": format_month_year(start_val),
            "end": end_val,
            "end_display": format_month_year(end_val) if end_val != "Present" else "Present",
            "desc": desc_list[:3], # Limit to 3 bullets for layout
        })

    # ---------- PROJECTS ----------
    projects = []
    proj_names = get_list("proj_name[]")
    proj_stacks = get_list("proj_stack[]")
    proj_descs = get_list("proj_desc[]")
    
    for i in range(len(proj_names)):
        if i >= len(proj_names): break
        desc_list = text_to_bullets(proj_descs[i]) if i < len(proj_descs) else []
        
        projects.append({
            "name": proj_names[i],
            "stack": proj_stacks[i] if i < len(proj_stacks) else "",
            "desc": desc_list[:3],
        })

    # ---------- CERTIFICATIONS ----------
    certifications = []
    cert_names = get_list("cert_name[]")
    cert_orgs = get_list("cert_org[]")
    
    for i in range(len(cert_names)):
        if i >= len(cert_names): break
        certifications.append({
            "name": cert_names[i],
            "org": cert_orgs[i] if i < len(cert_orgs) else "",
        })

    # ---------- ACHIEVEMENTS ----------
    achievements = []
    ach_titles = get_list("ach_title[]")
    ach_orgs = get_list("ach_org[]")
    ach_dates = get_list("ach_date[]")
    ach_descs = get_list("ach_desc[]")

    for i in range(len(ach_titles)):
        if i >= len(ach_titles): break
        achievements.append({
            "title": ach_titles[i],
            "org": ach_orgs[i] if i < len(ach_orgs) else "",
            "date": format_month_year(ach_dates[i]) if i < len(ach_dates) else "",
            "desc": ach_descs[i] if i < len(ach_descs) else "",
        })

    # ---------- HOBBIES ----------
    hobbies = []
    hobby_names = get_list("hobby_name[]")
    hobby_descs = get_list("hobby_desc[]")

    for i in range(len(hobby_names)):
        if i >= len(hobby_names): break
        hobbies.append({
            "name": hobby_names[i],
            "desc": hobby_descs[i] if i < len(hobby_descs) else "",
        })

    # ---------- CONTEXT ASSEMBLY ----------
    context = {
        "full_name": request.POST.get("full_name"),
        "email": request.POST.get("email"),
        "phone": request.POST.get("phone"),
        "linkedin": request.POST.get("linkedin"),
        "github": request.POST.get("github"),
        "portfolio": request.POST.get("portfolio"),
        "summary": shorten_summary(request.POST.get("summary", "")),
        "skills_raw": request.POST.get("skills", ""),
        "skills_flat": [s.strip() for s in request.POST.get("skills", "").split(",") if s.strip()],
        "skills": categorize_skills(request.POST.get("skills", "")),
        "show_skill_categories": request.POST.get("show_skill_categories") == "on",
        "education": education,
        "experience": experience,
        "projects": projects,
        "certifications": certifications,
        "achievements": achievements,
        "hobbies": hobbies,
    }

    # Store in session as the single source of truth
    request.session["resume_data"] = context

    # Handle Next Action
    if request.POST.get("action") == "preview":
        return redirect("resume_preview")
    else:
        return redirect("resume_download")


def resume_preview(request):
    """
    Renders a clean HTML preview of the resume.
    """
    data = request.session.get("resume_data")
    if not data:
        return redirect("resume_builder")

    return render(request, "core/resume_builder/resume_preview.html", data)


def resume_download(request):
    """
    Generates and returns the PDF resume.
    """
    data = request.session.get("resume_data")
    if not data:
        return redirect("resume_builder")

    # Use our centralized PDF generator
    response = render_resume_pdf("core/resume_builder/resume_pdf.html", data)
    
    if not response:
        return HttpResponse("Error generating PDF", status=500)
        
    return response


def resume_edit(request):
    """
    Redirects back to the builder form (data is already in session).
    """
    return redirect("resume_builder")
