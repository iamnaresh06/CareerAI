"""
Career Chatbot Logic for CareerAI.

This module implements a hybrid chatbot using the modern Google GenAI SDK (v2).
It searches a local knowledge base (JSON) first and falls back to Gemini AI.

Author: Naresh Reddy (Updated April 2026)
"""

import os
import json
from google import genai
from dotenv import load_dotenv
from .ml_engine import calculate_text_similarity

# Load environment variables
env_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "..", ".env"))
load_dotenv(dotenv_path=env_path)

# Path to the local knowledge base
KB_FILE_PATH = os.path.join(os.path.dirname(__file__), 'data', 'educational_kb.json')

# Configure Gemini Client
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")

def get_ai_client():
    """Initializes the new Google GenAI client."""
    if not GEMINI_API_KEY or GEMINI_API_KEY == "your_gemini_api_key_here":
        return None
    try:
        # Using the modern GenAI Client (v2 SDK)
        return genai.Client(api_key=GEMINI_API_KEY)
    except Exception as e:
        print(f"DEBUG: GenAI Client Init Error: {e}")
        return None

# Initial client setup
client = get_ai_client()

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


def search_local_kb(query, threshold=70.0):
    """
    Searches the local JSON knowledge base for a similar question.
    """
    if not os.path.exists(KB_FILE_PATH):
        return None, 0

    try:
        with open(KB_FILE_PATH, 'r') as f:
            kb_data = json.load(f)
        
        best_match = None
        highest_score = 0

        for item in kb_data:
            score = calculate_text_similarity(query, item['question'])
            if score > highest_score:
                highest_score = score
                best_match = item['answer']
        
        if highest_score >= threshold:
            return best_match, highest_score
            
    except Exception as e:
        print(f"Error reading KB: {e}")
    
    return None, 0


def add_to_local_kb(question, answer):
    """
    Auto-learning: Saves new AI answers to the local knowledge base to reduce API calls.
    Only saves meaningful questions (more than 2 words).
    """
    if len(question.strip().split()) < 3:
        return

    try:
        kb_data = []
        if os.path.exists(KB_FILE_PATH):
            with open(KB_FILE_PATH, 'r') as f:
                kb_data = json.load(f)
        
        # Avoid semantic duplicates using our AI similarity engine
        for item in kb_data:
            score = calculate_text_similarity(question.strip(), item['question'])
            if score > 85.0:  # If we already have a 85% similar question, don't duplicate
                return
                
        kb_data.append({
            "question": question.strip(),
            "answer": answer.strip()
        })
        
        with open(KB_FILE_PATH, 'w', encoding='utf-8') as f:
            json.dump(kb_data, f, indent=4)
    except Exception as e:
        print(f"DEBUG: Failed to update KB: {e}")



def get_chatbot_response(user_message, resume_score=None, missing_skills=None):
    """
    Main response logic using GenAI Fallback.
    """
    global client
    msg = user_message.strip()

    # Runtime initialization check
    if client is None:
        client = get_ai_client()

    # 1. Local Search
    local_answer, confidence = search_local_kb(msg)
    if local_answer:
        return f"{local_answer}\n\n✅ Verified Educational Answer"

    # 2. AI Fallback (New GenAI API)
    if client:
        try:
            # Construct the system instruction and prompt
            system_instruction = (
                "You are CareerAI, a friendly and encouraging career mentor for students. "
                "RULES: "
                "1. If the user simply says a greeting (e.g., 'Hi', 'Hello'), politely say hello back and ask how you can help them with their career. "
                "2. For specific career/tech questions, give direct, actionable advice using 3-4 short bullet points. Do not write long essays. "
                "3. Be warm and supportive, but keep answers extremely concise. "
                "4. Only answer tech, career, and education-related questions."
            )
            
            context = ""
            if resume_score:
                context += f"- Resume Score: {resume_score}%.\n"
            if missing_skills:
                context += f"- Missing Skills: {', '.join(missing_skills)}.\n"

            # STEP 2.1: Try the most efficient model for Free Tier (3.1 Lite)
            try:
                response = client.models.generate_content(
                    model="gemini-3.1-flash-lite-preview",
                    contents=f"{system_instruction}\n\n{context}\nQuestion: {msg}"
                )
                answer = response.text
                add_to_local_kb(msg, answer)
                return answer
            except Exception as e:
                # STEP 2.2: Second AI Fallback (2.0 Flash)
                print(f"DEBUG: 3.1 Lite Failed, trying 2.0 Flash: {e}")
                response = client.models.generate_content(
                    model="gemini-2.0-flash",
                    contents=f"{system_instruction}\n\n{context}\nQuestion: {msg}"
                )
                answer = response.text
                add_to_local_kb(msg, answer)
                return answer
        except Exception as e:
            print(f"DEBUG: All AI Models Failed: {e}")

    # 3. Last Fallback: Role Logic
    msg_lower = msg.lower()
    if any(word in msg_lower for word in ["roadmap", "road map", "path"]):
        for role in CAREER_ROLES:
            if role in msg_lower:
                data = CAREER_ROLES[role]
                return f"📌 Roadmap for {role.title()}:\n\n- Skills: {', '.join(data['skills'])}\n- Path: {data['path']}"

    return (
        "👋 Hi! I'm your CareerAI Assistant. I'm currently optimizing my AI connection. "
        "Try asking: 'Roadmap for Python Developer' or specialized tech career questions!"
    )