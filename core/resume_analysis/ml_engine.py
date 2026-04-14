"""
Machine Learning Engine for CareerAI.

This module handles all NLP (Natural Language Processing) tasks, including:
1. Skill Extraction using keyword matching.
2. Text Similarity Calculation using TF-IDF and Cosine Similarity.
3. Resume Scoring logic based on job descriptions.
4. Feedback Generation based on calculated scores.

Dependencies:
    - scikit-learn (TfidfVectorizer, cosine_similarity)
    - numpy

Author: Naresh Reddy
"""

import re


# -----------------------------------------------------------------------------
# Skill Knowledge Base
# -----------------------------------------------------------------------------
# Dictionary mapping canonical skill names to potential variations/aliases found in text.
SKILL_ALIASES = {
    # Programming Languages
    "python": ["python"],
    "java": ["java", "core java"],
    "c": ["c language"],
    "c++": ["c++", "cpp"],
    "c#": ["c#", "dotnet"],
    "javascript": ["javascript", "js"],
    "typescript": ["typescript", "ts"],
    "php": ["php"],
    "r": ["r programming"],
    "go": ["golang", "go language"],
    "ruby": ["ruby"],

    # Web Technologies
    "html": ["html", "html5"],
    "css": ["css", "css3"],
    "bootstrap": ["bootstrap"],
    "tailwind css": ["tailwind", "tailwind css"],
    "jquery": ["jquery"],

    # Frameworks & Libraries
    "django": ["django"],
    "flask": ["flask"],
    "fastapi": ["fastapi"],
    "spring": ["spring", "spring boot"],
    "react": ["react", "reactjs"],
    "angular": ["angular", "angularjs"],
    "vue": ["vue", "vuejs"],
    "node.js": ["node", "nodejs"],
    "express.js": ["express", "expressjs"],

    # Databases
    "sql": ["sql"],
    "mysql": ["mysql"],
    "postgresql": ["postgresql", "postgres"],
    "mongodb": ["mongodb", "mongo"],
    "sqlite": ["sqlite"],
    "oracle": ["oracle db", "oracle"],

    # Data Science & AI
    "machine learning": ["machine learning", "ml"],
    "deep learning": ["deep learning", "dl"],
    "data analysis": ["data analysis", "data analytics"],
    "nlp": ["nlp", "natural language processing"],
    "computer vision": ["computer vision", "opencv"],
    "tensorflow": ["tensorflow"],
    "pytorch": ["pytorch"],
    "numpy": ["numpy"],
    "pandas": ["pandas"],
    "scikit-learn": ["scikit-learn", "sklearn"],

    # DevOps & Tools
    "git": ["git", "github", "gitlab"],
    "docker": ["docker"],
    "kubernetes": ["kubernetes", "k8s"],
    "jenkins": ["jenkins"],
    "linux": ["linux", "ubuntu", "centos"],
    "bash": ["bash", "shell scripting"],

    # Cloud Platforms
    "aws": ["aws", "amazon web services"],
    "azure": ["azure", "microsoft azure"],
    "gcp": ["gcp", "google cloud"],
    "render": ["render"],
    "heroku": ["heroku"],

    # APIs & Architecture
    "rest api": ["rest api", "restful api"],
    "graphql": ["graphql"],
    "microservices": ["microservices"],
    "mvc": ["mvc architecture"],

    # Testing & QA
    "unit testing": ["unit testing"],
    "selenium": ["selenium"],
    "pytest": ["pytest"],
    "junit": ["junit"],

    # Mobile Development
    "android": ["android"],
    "ios": ["ios"],
    "flutter": ["flutter"],
    "react native": ["react native"],

    # Soft / Non-Technical Skills
    "communication": ["communication skills", "verbal communication"],
    "teamwork": ["teamwork", "team player"],
    "problem solving": ["problem solving", "analytical thinking"],
    "leadership": ["leadership"],
    "time management": ["time management"],
    "critical thinking": ["critical thinking"],
    "adaptability": ["adaptability", "flexibility"],
    "project management": ["project management"],
}


# -----------------------------------------------------------------------------
# Core Functions
# -----------------------------------------------------------------------------

def extract_skills(text):
    """
    Scans the input text for known skills defined in SKILL_ALIASES.
    
    Args:
        text (str): The raw text (e.g., resume content or job description).
        
    Returns:
        list: A list of unique canonical skill names found in the text.
    """
    text = text.lower()
    found = []

    for skill, aliases in SKILL_ALIASES.items():
        for alias in aliases:
            # Ensure whole word match to avoid substring issues (e.g., 'java' in 'javascript')
            # (?<!\w) and (?!\w) are used instead of \b to correctly handle special characters like C++ or C#
            pattern = r'(?<!\w)' + re.escape(alias) + r'(?!\w)'
            if re.search(pattern, text):
                found.append(skill)
                break

    return found


def calculate_text_similarity(resume_text, job_description):
    """
    Computes the cosine similarity between two text documents using TF-IDF.
    
    Args:
        resume_text (str): Content of the resume.
        job_description (str): Content of the job description.
        
    Returns:
        float: Similarity percentage (0.0 to 100.0).
    """
    if not resume_text or not job_description:
        return 0.0

    from sklearn.feature_extraction.text import TfidfVectorizer
    from sklearn.metrics.pairwise import cosine_similarity

    vectorizer = TfidfVectorizer(
        stop_words='english',
        ngram_range=(1, 2)  # Consider unigrams and bigrams
    )

    try:
        tfidf = vectorizer.fit_transform([resume_text, job_description])
        similarity = cosine_similarity(tfidf[0:1], tfidf[1:2])
        return round(similarity[0][0] * 100, 2)
    except ValueError:
        # Handles cases with empty vocabulary or stop words issues
        return 0.0


def get_missing_skills(resume_text, job_description):
    """
    Identifies skills present in the job description but missing from the resume.
    
    Args:
        resume_text (str): Content of the resume.
        job_description (str): Content of the job description.
        
    Returns:
        list: Skills found in JD but not in Resume.
    """
    resume_skills = extract_skills(resume_text)
    job_skills = extract_skills(job_description)

    return list(set(job_skills) - set(resume_skills))


def calculate_skill_score(resume_text, job_description):
    """
    Calculates a score based on the intersection of skills.
    
    Args:
        resume_text (str): Content of the resume.
        job_description (str): Content of the job description.
        
    Returns:
        float: Percentage of JD skills found in Resume.
    """
    resume_text = resume_text.lower()
    job_description = job_description.lower()

    jd_skills = extract_skills(job_description)
    resume_skills = extract_skills(resume_text)

    if not jd_skills:
        return 0.0

    matched = set(jd_skills).intersection(set(resume_skills))
    score = (len(matched) / len(jd_skills)) * 100

    return round(score, 2)


def calculate_final_score(resume_text, job_description):
    """
    Computes the final weighted score combining skill matching and text similarity.
    
    Logic:
        - Skill Match: 70% weight (Critical for ATS)
        - Context/Text Similarity: 30% weight
        
    Args:
        resume_text (str): Content of the resume.
        job_description (str): Content of the job description.
        
    Returns:
        tuple: (final_score, skill_score, text_score)
    """
    skill_score = calculate_skill_score(resume_text, job_description)
    text_score = calculate_text_similarity(resume_text, job_description)

    # Weighted score calculation
    final_score = (0.7 * skill_score) + (0.3 * text_score)

    return round(final_score, 2), skill_score, text_score


def generate_feedback_message(final_score, skill_score, missing_skills):
    """
    Generates a human-readable feedback message based on the analysis.
    
    Args:
        final_score (float): The overall match percentage.
        skill_score (float): The skill-specific match percentage.
        missing_skills (list): List of missing skills.
        
    Returns:
        str: A descriptive feedback string.
    """
    final_score = float(final_score)
    skill_score = float(skill_score)

    message = ""

    # Determine feedback tier
    if final_score >= 75 or (final_score >= 70 and skill_score >= 60):
        message = (
            "Strong match. Your resume aligns well with the job requirements. "
            "You have a high probability of being shortlisted."
        )
    elif final_score >= 50:
        message = (
            "Good match. Your resume meets most of the key requirements, "
            "but adding a few more specific skills could significantly improve your chances."
        )
    else:
        message = (
            "Low match. Your resume currently lacks critical keywords found in the job description. "
            "We recommend tailoring it further by adding the highlighted missing skills."
        )

    # Append missing skills context
    if missing_skills:
        # Limit to top 5 to avoid overwhelming the user
        top_missing = missing_skills[:5]
        skills_text = ", ".join(top_missing)
        message += f" Key missing skills to consider adding: {skills_text}."

    return message