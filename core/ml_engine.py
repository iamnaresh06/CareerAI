from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


# central skill list used everywhere

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




def extract_skills(text):
    text = text.lower()
    found = []

    for skill, aliases in SKILL_ALIASES.items():
        for alias in aliases:
            if alias in text:
                found.append(skill)
                break

    return found



def calculate_text_similarity(resume_text, job_description):
    vectorizer = TfidfVectorizer(
        stop_words='english',
        ngram_range=(1, 2)
    )

    tfidf = vectorizer.fit_transform([resume_text, job_description])
    similarity = cosine_similarity(tfidf[0:1], tfidf[1:2])

    return round(similarity[0][0] * 100, 2)



def get_missing_skills(resume_text, job_description):
    resume_skills = extract_skills(resume_text)
    job_skills = extract_skills(job_description)

    return list(set(job_skills) - set(resume_skills))


def calculate_skill_score(resume_text, job_description):
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
    skill_score = calculate_skill_score(resume_text, job_description)
    text_score = calculate_text_similarity(resume_text, job_description)

    # weighted score (ATS-style)
    final_score = (0.7 * skill_score) + (0.3 * text_score)

    return round(final_score, 2), skill_score, text_score