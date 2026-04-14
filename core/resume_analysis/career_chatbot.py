"""
Career Chatbot Logic for CareerAI.

This module implements a rule-based chatbot that guides freshers through career choices,
provides learning roadmaps, suggests projects, and answers common interview questions.

It is designed to be deterministic and helpful for specific fresher-level queries.

Author: Naresh Reddy
"""

CAREER_ROLES = {
    "python developer": {
        "skills": ["python", "oops", "django", "sql", "git"],
        "path": "Python Basics → OOP → Django → REST APIs → Projects",
        "projects": [
            "Student Management System",
            "To-Do Web Application",
            "Resume Analyzer Web App",
            "Blog Application using Django",
            "REST API for Notes App"
        ],
        "interview": [
            "What is Python?",
            "Explain OOP concepts",
            "What is Django MVT?",
            "What is ORM?",
            "Difference between list and tuple"
        ]
    },

    "data analyst": {
        "skills": ["python", "sql", "excel", "pandas", "matplotlib"],
        "path": "Excel → SQL → Python → Pandas → Data Visualization",
        "projects": [
            "Sales Data Analysis using Excel",
            "COVID-19 Data Analysis",
            "Student Performance Analysis",
            "Exploratory Data Analysis using Pandas",
            "Dashboard using Matplotlib"
        ],
        "interview": [
            "What is data analysis?",
            "Explain SQL joins",
            "What is data cleaning?",
            "What is pandas?",
            "Difference between mean and median"
        ]
    },

    "frontend developer": {
        "skills": ["html", "css", "javascript", "react"],
        "path": "HTML → CSS → JavaScript → React → Projects",
        "projects": [
            "Responsive Portfolio Website",
            "To-Do App using JavaScript",
            "Weather App using API",
            "React Blog Application",
            "UI Clone of a Popular Website"
        ],
        "interview": [
            "What is HTML?",
            "CSS box model",
            "Difference between var, let, const",
            "What are React hooks?",
            "What is Virtual DOM?"
        ]
    },

    "backend developer": {
        "skills": ["python", "django", "rest api", "sql"],
        "path": "Python → Django → REST APIs → Authentication → Deployment",
        "projects": [
            "Authentication System",
            "REST API for E-commerce",
            "User Management System",
            "Backend for Chat Application",
            "API for Resume Analyzer"
        ],
        "interview": [
            "What is REST API?",
            "Explain HTTP methods",
            "What is authentication?",
            "Difference between GET and POST"
        ]
    },

    "full stack developer": {
        "skills": ["html", "css", "javascript", "react", "django", "sql"],
        "path": "Frontend Basics → Backend → APIs → Full Stack Projects",
        "projects": [
            "Job Portal Application",
            "Learning Management System",
            "E-commerce Website",
            "Career Guidance Platform",
            "Chat Application"
        ],
        "interview": [
            "Explain frontend vs backend",
            "What is REST?",
            "How frontend communicates with backend?",
            "What is MVC?"
        ]
    }
}


def get_chatbot_response(user_message, resume_score=None, missing_skills=None):
    """
    Generates a response based on keywords in the user's message.
    
    Args:
        user_message (str): The input text from the user.
        resume_score (float, optional): Context from resume analysis session.
        missing_skills (list, optional): Context from resume analysis session.
        
    Returns:
        str: The chatbot's response text.
    """
    msg = user_message.lower().strip()

    # -------------------------------------------------------------------------
    # Intent: Roadmap / Learning Path
    # -------------------------------------------------------------------------
    if any(word in msg for word in ["roadmap", "road map", "learning path", "path"]):
        for role in CAREER_ROLES:
            if role in msg:
                data = CAREER_ROLES[role]
                return (
                    f"📌 Roadmap for {role.title()} (Fresher Level):\n\n"
                    f"1 Required Skills:\n"
                    f"- " + "\n- ".join(data["skills"]) + "\n\n"
                    f"2 Step-by-Step Learning Path:\n"
                    f"{data['path']}\n\n"
                    f"3 Practical Advice:\n"
                    f"- Build small projects at each step\n"
                    f"- Focus more on fundamentals\n"
                    f"- Avoid jumping into advanced topics too early\n\n"
                    f"If you want, I can also give interview questions or project ideas for this role."
                )

        return (
            "Sure 👍 I can help you with a career roadmap.\n\n"
            "Please tell me **which role** you are interested in.\n\n"
            "Popular fresher roles:\n"
            "- Python Developer\n"
            "- Data Analyst\n"
            "- Frontend Developer"
        )

    # -------------------------------------------------------------------------
    # Intent: Interview Questions
    # -------------------------------------------------------------------------
    if "interview" in msg:
        for role in CAREER_ROLES:
            if role in msg:
                questions = CAREER_ROLES[role]["interview"]
                return (
                    f"🧠 Interview Questions for {role.title()} (Freshers):\n\n"
                    + "\n".join([f"{i+1}. {q}" for i, q in enumerate(questions)]) +
                    "\n\n📌 Tip:\n"
                    "- Understand concepts, don’t memorize answers\n"
                    "- Try explaining answers in your own words\n\n"
                    "If you want, I can also help you with answers or mock interview tips."
                )

        return (
            "I can share interview questions \n\n"
            "Please mention the role.\n"
            "Example:\n"
            "- Django interview questions for freshers\n"
            "- Data Analyst interview questions"
        )

    # -------------------------------------------------------------------------
    # Intent: General Career / Role Guidance
    # -------------------------------------------------------------------------
    if any(word in msg for word in ["career", "role", "job", "future"]):
        response = "🎯 Career Guidance for Freshers:\n\n"

        if resume_score:
            if resume_score >= 75:
                response += (
                    "Your resume score is good \n"
                    "You are ready to apply for entry-level developer roles.\n\n"
                )
            else:
                response += (
                    "Your resume needs some improvement, which is normal for freshers.\n"
                    "Focus on skills and projects before applying.\n\n"
                )

        response += (
            "Recommended fresher-friendly roles:\n"
            "- Python Developer\n"
            "- Data Analyst\n"
            "- Frontend Developer\n\n"
            "Tell me which role you like, and I’ll guide you step-by-step."
        )

        return response

    # -------------------------------------------------------------------------
    # Intent: Skill Improvement
    # -------------------------------------------------------------------------
    if "skill" in msg or "improve" in msg:
        if missing_skills:
            return (
                "Skill Improvement Guidance:\n\n"
                "Based on your resume, you should focus on these skills:\n"
                "- " + "\n- ".join(missing_skills) + "\n\n"
                "How to improve:\n"
                "- Start with basics\n"
                "- Practice daily (even 30–60 mins)\n"
                "- Build 1–2 small projects\n\n"
                "If you want, I can create a learning plan for any one skill."
            )

        return (
            "To improve skills, choose a target role first.\n"
            "Then I can suggest exact skills and a learning plan."
        )
    
    # -------------------------------------------------------------------------
    # Intent: Project Ideas
    # -------------------------------------------------------------------------
    if "project" in msg or "build" in msg:
        for role in CAREER_ROLES:
            if role in msg:
                projects = CAREER_ROLES[role]["projects"]
                return (
                    f"💡 Project Suggestions for {role.title()} (Freshers):\n\n"
                    + "\n".join([f"{i+1}. {p}" for i, p in enumerate(projects)])
                    + "\n\n📌 Advice:\n"
                    "- Start with simple projects\n"
                    "- Focus on logic, not UI\n"
                    "- Push projects to GitHub\n\n"
                    "If you want, I can suggest projects based on your current skills."
                )

        return (
            "Sure 👍 I can suggest projects.\n\n"
            "Please mention the role.\n"
            "Example:\n"
            "- Projects for Python Developer\n"
            "- Frontend projects for freshers"
        )

    # -------------------------------------------------------------------------
    # Intent: Emotional / Confusion Support
    # -------------------------------------------------------------------------
    if any(word in msg for word in ["confused", "don’t know", "not sure", "help"]):
        return (
            "That’s completely normal 🙂 Many freshers feel the same.\n\n"
            "Let’s do this step-by-step:\n"
            "1 Choose a role you like\n"
            "2 Learn required skills\n"
            "3 Build small projects\n"
            "4 Prepare for interviews\n\n"
            "Tell me what you are confused about, I’ll help you."
        )

    # -------------------------------------------------------------------------
    # Default Response
    # -------------------------------------------------------------------------
    return (
        "👋 Hi! I’m your CareerAI Assistant.\n\n"
        "I can help you with:\n"
        "- Career roadmaps\n"
        "- Learning paths\n"
        "- Skill improvement\n"
        "- Interview questions\n\n"
        "Try asking:\n"
        "• Roadmap for Python Developer\n"
        "• What skills should I learn next?\n"
        "• Interview questions for Django fresher"
    )