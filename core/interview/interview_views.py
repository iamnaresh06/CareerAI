"""
Interview Views for CareerAI.

This module manages the AI Mock Interview sessions.
It handles:
1. Session Initialization (Topic Selection).
2. Question Delivery.
3. Answer Processing (Speech-to-Text Analysis via API).

Author: Naresh Reddy
"""

from django.shortcuts import render
from django.http import JsonResponse
from core.interview.engine import get_questions_by_category, analyze_interview_response, INTERVIEW_QUESTIONS
import json
import random

def interview_hub(request):
    """
    Renders the interview topic selection hub.
    Displays available categories like Python, Django, Behavioral, etc.
    """
    categories = INTERVIEW_QUESTIONS.keys()
    context = {"categories": categories}
    return render(request, "core/interview/hub.html", context)


def start_interview(request, category):
    """
    Initializes a new interview session for a selected category.
    """
    questions = get_questions_by_category(category)
    
    if not questions:
        # Fallback if an invalid category is accessed via URL
        return render(request, "core/interview/hub.html", {"error": "Category not found"})
    
    # Shuffle questions to ensure variety in every session
    # Using a copy to avoid mutating the original global list
    questions_list = list(questions)
    random.shuffle(questions_list)
    
    # Pass questions as JSON for client-side JavaScript handling
    context = {
        "category": category,
        "questions": json.dumps(questions_list), 
    }
    return render(request, "core/interview/session.html", context)


def process_answer(request):
    """
    API Endpoint: Analyzes a user's spoken answer.
    
    Expects JSON payload:
    {
        "answer": "User's transcribed text",
        "question_id": 123,
        "category": "python"
    }
    
    Returns JSON:
    {
        "score": 85.5,
        "feedback": "Great answer...",
        "missing_keywords": ["mutable"]
    }
    """
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            user_text = data.get("answer", "")
            question_id = data.get("question_id")
            category = data.get("category")
            
            if not user_text:
                return JsonResponse({"error": "No answer provided"}, status=400)
                
            # Perform Analysis using the Interview Engine
            result = analyze_interview_response(user_text, question_id, category)
            
            return JsonResponse(result)
            
        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON"}, status=400)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)
            
    return JsonResponse({"error": "Invalid request method"}, status=405)
