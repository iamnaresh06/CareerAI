"""
AI Interview Engine for CareerAI.

This module powers the mock interview feature. It handles:
1. Question Bank Management (Categorized questions with ideal answers).
2. Answer Analysis using NLP (Cosine Similarity + Keyword Matching).
3. Scoring and Feedback Generation.

Dependencies:
    - scikit-learn (TfidfVectorizer, cosine_similarity)
    - re (Regular Expressions)

Author: Naresh Reddy
"""

import re


# -----------------------------------------------------------------------------
# Question Bank
# -----------------------------------------------------------------------------
INTERVIEW_QUESTIONS = {
    "python": [
        {
            "id": 1,
            "question": "What are the key differences between Python lists and tuples?",
            "ideal_answer": "Lists are mutable, meaning they can be changed after creation, while tuples are immutable and cannot be modified. Lists use square brackets and tuples use parentheses. Tuples are generally faster and safer for read-only data.",
            "keywords": ["mutable", "immutable", "brackets", "parentheses", "faster", "change"]
        },
        {
            "id": 2,
            "question": "Explain the concept of decorators in Python.",
            "ideal_answer": "Decorators are functions that modify the behavior of other functions or methods. They allow you to wrap another function in order to extend the behavior of the wrapped function, without permanently modifying it. They use the @ symbol.",
            "keywords": ["modify", "behavior", "wrap", "extend", "@ symbol", "function"]
        },
         {
            "id": 3,
            "question": "What is the difference between shallow copy and deep copy?",
            "ideal_answer": "A shallow copy creates a new object but inserts references into it. A deep copy creates a new object and recursively adds copies of the objects found in the original. Deep copy is used when you want a completely independent copy.",
            "keywords": ["reference", "recursive", "independent", "copy module", "nested"]
        }
    ],
    "django": [
        {
            "id": 4,
            "question": "Explain the MVT architecture in Django.",
            "ideal_answer": "MVT stands for Model-View-Template. Model handles the database and data structure. View handles the business logic and interacts with the model. Template handles the user interface and presentation layer using HTML.",
            "keywords": ["model", "view", "template", "database", "logic", "presentation", "html"]
        },
        {
            "id": 5,
            "question": "What are Django signals?",
            "ideal_answer": "Signals are a way to allow decoupled applications to get notified when certain actions occur elsewhere in the framework. For example, post_save signal is sent when a model instance is saved.",
            "keywords": ["decoupled", "notified", "actions", "post_save", "receiver", "sender"]
        }
    ],
    "behavioral": [
        {
            "id": 6,
            "question": "Tell me about a time you faced a difficult technical challenge.",
            "ideal_answer": "I once faced a complex bug in a production database migration. I analyzed the logs, identified the root cause as a data inconsistency, and wrote a script to clean the data before re-running the migration. It taught me the importance of testing migrations on staging.",
            "keywords": ["challenge", "bug", "analyzed", "solution", "learned", "result"]
        },
        {
            "id": 7,
            "question": "Where do you see yourself in 5 years?",
            "ideal_answer": "I see myself as a Senior Developer or Tech Lead, having mastered full-stack development and contributed to scalable system architectures. I also want to mentor junior developers.",
            "keywords": ["senior", "lead", "mastered", "architectures", "mentor", "growth"]
        }
    ]
}

# -----------------------------------------------------------------------------
# Core Functions
# -----------------------------------------------------------------------------

def get_questions_by_category(category):
    """
    Retrieves a list of interview questions for a specific topic.
    
    Args:
        category (str): The topic name (e.g., 'python', 'django').
        
    Returns:
        list: List of question dictionaries.
    """
    return INTERVIEW_QUESTIONS.get(category.lower(), [])


def analyze_interview_response(user_text, question_id, category):
    """
    Analyzes the user's spoken response against the ideal answer.
    
    Algorithm:
    1. Retrieve the ideal answer and required keywords for the question.
    2. Calculate Cosine Similarity score (Semantic Match).
    3. Calculate Keyword Coverage score (Technical Accuracy).
    4. Compute weighted average score.
    5. Generate feedback based on score thresholds.
    
    Args:
        user_text (str): The transcribed user answer.
        question_id (int): The ID of the question being answered.
        category (str): The category of the question.
        
    Returns:
        dict: detailed analysis including score, feedback, and missing keywords.
    """
    
    # 1. content fetching
    questions = INTERVIEW_QUESTIONS.get(category.lower(), [])
    # Find the specific question by ID
    question_data = next((q for q in questions if q["id"] == int(question_id)), None)
    
    if not question_data:
        return {"error": "Question not found"}

    ideal_answer = question_data["ideal_answer"]
    
    # 2. Similarity Score (Cosine Similarity)
    # Using TF-IDF to convert text to vectors and finding cosine angle between them
    try:
        from sklearn.feature_extraction.text import TfidfVectorizer
        from sklearn.metrics.pairwise import cosine_similarity
        vectorizer = TfidfVectorizer(stop_words='english')
        tfidf = vectorizer.fit_transform([user_text, ideal_answer])
        similarity = cosine_similarity(tfidf[0:1], tfidf[1:2])[0][0]
    except ValueError:
        # Handle empty or stop-word-only inputs
        similarity = 0.0
    
    # Scale to 0-100
    similarity_score = similarity * 100
    
    # 3. Keyword Matching (Improved tokenization)
    user_text_lower = user_text.lower()
    
    # Simple regex to split text into words, removing punctuation
    user_tokens = set(re.findall(r'\b\w+\b', user_text_lower))
    
    required_keywords = question_data["keywords"]
    missing_keywords = []
    
    for kw in required_keywords:
        kw_lower = kw.lower()
        if ' ' not in kw_lower:
             # Single word: match strictly against token set
             if kw_lower not in user_tokens:
                 missing_keywords.append(kw)
        else:
            # Multi-word: match as a substring in the full text
            if kw_lower not in user_text_lower:
                missing_keywords.append(kw)
    
    # Calculate keyword coverage percentage
    total_keywords = len(required_keywords)
    matched_count = total_keywords - len(missing_keywords)
    keyword_coverage = matched_count / total_keywords if total_keywords > 0 else 1.0

    # Weighted Score: 40% Similarity + 60% Keyword Coverage
    # We prioritize keywords because technical answers need specific terminology
    final_score = (similarity_score * 0.4) + (keyword_coverage * 100 * 0.6)
    score = round(final_score, 1)

    # 4. Generate Feedback
    feedback = ""
    
    if score >= 75:
        feedback = "Excellent! You covered almost all key concepts clearly."
    elif score >= 40:
        feedback = "Good attempt. Try to include more specific technical terms mentioned below."
    else:
        feedback = "Detailed answer required. Please review the missing keywords and try again."
        
    return {
        "score": score,
        "feedback": feedback,
        "missing_keywords": missing_keywords,
        "ideal_answer": ideal_answer
    }
