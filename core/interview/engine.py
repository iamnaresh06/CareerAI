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
# -----------------------------------------------------------------------------
# Category Configuration (Priority Order)
# -----------------------------------------------------------------------------
INTERVIEW_CATEGORIES = [
    {
        "id": "programming",
        "name": "Programming Languages",
        "icon": "fas fa-code",
        "skills": [
            {"id": "python", "name": "Python", "icon": "🐍", "desc": "Object-oriented, interpreted, high-level language."},
            {"id": "java", "name": "Java", "icon": "☕", "desc": "Class-based, object-oriented, write once run anywhere."},
            {"id": "javascript", "name": "JavaScript", "icon": "📜", "desc": "Core language for web interactivity and Node.js."},
            {"id": "cpp", "name": "C++", "icon": "⚙️", "desc": "High-performance language for systems and games."},
            {"id": "c", "name": "C", "icon": "🧱", "desc": "Low-level language for firmware and OS development."},
            {"id": "golang", "name": "Go (Golang)", "icon": "🐹", "desc": "Google's open-source language for cloud scale."},
            {"id": "rust", "name": "Rust", "icon": "⚙️", "desc": "Safe, concurrent, and high-performance language."}
        ]
    },
    {
        "id": "web",
        "name": "Web Technologies",
        "icon": "fas fa-globe",
        "skills": [
            {"id": "html_css", "name": "HTML & CSS", "icon": "🎨", "desc": "Building the structure and design of the web."},
            {"id": "react", "name": "React.js", "icon": "⚛️", "desc": "Facebook's frontend library for UI components."},
            {"id": "nextjs", "name": "Next.js", "icon": "🔳", "desc": "React framework for production with SSR."},
            {"id": "angular", "name": "Angular", "icon": "🅰️", "desc": "Google's platform for building mobile and web apps."},
            {"id": "nodejs", "name": "Node.js", "icon": "🟢", "desc": "JavaScript runtime for scalable backend services."}
        ]
    },
    {
        "id": "frameworks",
        "name": "Frameworks",
        "icon": "fas fa-cubes",
        "skills": [
            {"id": "django", "name": "Django", "icon": "🎸", "desc": "Python-based high-level web framework."},
            {"id": "springboot", "name": "Spring Boot", "icon": "🍃", "desc": "Java framework for production-grade apps."},
            {"id": "flask", "name": "Flask", "icon": "🧪", "desc": "Python micro web framework."},
            {"id": "express", "name": "Express.js", "icon": "🚈", "desc": "Minimalist web framework for Node.js."}
        ]
    },
    {
        "id": "core_cs",
        "name": "Core CS & Systems",
        "icon": "fas fa-microchip",
        "skills": [
            {"id": "dsa", "name": "Data Structures & Algorithms", "icon": "📑", "desc": "Fundamental computer science patterns."},
            {"id": "databases", "name": "Databases (SQL/NoSQL)", "icon": "💾", "desc": "Data storage, relational and document stores."},
            {"id": "system_design", "name": "System Design", "icon": "🏗️", "desc": "Designing scalable architectures."}
        ]
    },
    {
        "id": "cloud_ai",
        "name": "Cloud, AI & Testing",
        "icon": "fas fa-cloud",
        "skills": [
            {"id": "devops", "name": "Cloud & DevOps", "icon": "☁️", "desc": "AWS, Docker, Jenkins and CI/CD."},
            {"id": "aiml", "name": "AI & Machine Learning", "icon": "🤖", "desc": "Deep learning, NLP and Generative AI."},
            {"id": "testing", "name": "Software Testing", "icon": "🧪", "desc": "QA, Automation and Unit Testing."}
        ]
    },
    {
        "id": "hr",
        "name": "Behavioral & HR",
        "icon": "fas fa-users",
        "skills": [
            {"id": "behavioral", "name": "Behavioral Interviews", "icon": "👔", "desc": "STAR method and soft skills questions."}
        ]
    }
]

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
            "id": 101,
            "question": "What is Python's Global Interpreter Lock (GIL)?",
            "ideal_answer": "The GIL is a mutex that protects access to Python objects, preventing multiple native threads from executing Python bytecodes at once. This ensures thread safety but can limit performance in CPU-bound multi-threaded programs.",
            "keywords": ["GIL", "mutex", "native threads", "bytecodes", "thread safety", "CPU-bound"]
        }
    ],
    "java": [
        {
            "id": 201,
            "question": "What is the difference between JDK, JRE, and JVM?",
            "ideal_answer": "JVM runs the bytecode. JRE is JVM plus libraries to run apps. JDK is JRE plus tools like javac to develop apps.",
            "keywords": ["JVM", "JRE", "JDK", "bytecode", "libraries", "development kit"]
        },
        {
            "id": 202,
            "question": "Explain the concept of Abstraction in Java.",
            "ideal_answer": "Abstraction is the process of hiding implementation details and showing only functionality. It can be achieved using abstract classes and interfaces.",
            "keywords": ["hiding", "implementation", "functionality", "abstract", "interface"]
        }
    ],
    "javascript": [
        {
            "id": 301,
            "question": "What is a Closure in JavaScript?",
            "ideal_answer": "A closure is the combination of a function bundled together with references to its surrounding state (the lexical environment). It gives you access to an outer function's scope from an inner function.",
            "keywords": ["closure", "lexical environment", "scope", "bundled", "inner function"]
        },
        {
            "id": 302,
            "question": "Explain the difference between '==' and '===' operators.",
            "ideal_answer": "== is equality operator which performs type coercion. === is strict equality operator which checks both value and type without coercion.",
            "keywords": ["equality", "strict", "type coercion", "value", "type"]
        }
    ],
    "cpp": [
        {
            "id": 401,
            "question": "What are Pointers in C++?",
            "ideal_answer": "Pointers are variables that store the memory address of another variable. They are declared using the * operator and are fundamental for dynamic memory management.",
            "keywords": ["pointers", "memory address", "variables", "* operator", "dynamic memory"]
        }
    ],
    "golang": [
        {
            "id": 501,
            "question": "What are Goroutines in Go?",
            "ideal_answer": "Goroutines are lightweight threads managed by the Go runtime. They are used for concurrent execution and are much cheaper than OS threads.",
            "keywords": ["goroutines", "lightweight", "threads", "concurrent", "runtime"]
        }
    ],
    "react": [
        {
            "id": 601,
            "question": "Explain the Virtual DOM in React.",
            "ideal_answer": "Virtual DOM is a lightweight copy of the real DOM. When state changes, React updates the virtual DOM first, calculates the difference (diffing), and then updates only the necessary parts of the real DOM.",
            "keywords": ["virtual dom", "lightweight", "diffing", "reconciliation", "state change"]
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
    "dsa": [
        {
            "id": 701,
            "question": "What is the Time Complexity of searching in a Balanced Binary Search Tree?",
            "ideal_answer": "The time complexity is O(log n) because half of the tree is eliminated at each step of the search.",
            "keywords": ["O(log n)", "binary search tree", "balanced", "logarithmic", "efficiency"]
        }
    ],
    "databases": [
        {
            "id": 801,
            "question": "What is Database Normalization?",
            "ideal_answer": "Normalization is the process of organizing data to minimize redundancy and dependency. It involves dividing large tables into smaller ones and defining relationships between them.",
            "keywords": ["normalization", "redundancy", "dependency", "1NF", "2NF", "3NF"]
        }
    ],
    "devops": [
        {
            "id": 901,
            "question": "What is CI/CD?",
            "ideal_answer": "CI/CD stands for Continuous Integration and Continuous Deployment. It's a method to frequently deliver apps to customers by introducing automation into the stages of app development.",
            "keywords": ["automation", "integration", "deployment", "pipeline", "Jenkins", "GitLab"]
        }
    ],
    "aiml": [
        {
            "id": 1001,
            "question": "What is Overfitting in Machine Learning?",
            "ideal_answer": "Overfitting occurs when a model learns the training data too well, including the noise, resulting in poor performance on new, unseen data. It can be reduced using regularization or more data.",
            "keywords": ["overfitting", "noise", "generalization", "unseen data", "regularization", "training"]
        }
    ],
    "html_css": [
        {
            "id": 1101,
            "question": "What is the CSS Box Model?",
            "ideal_answer": "The CSS box model is a container that contains multiple properties, including borders, margin, padding, and the content itself. It is used to create the design and layout of web pages.",
            "keywords": ["border", "margin", "padding", "content", "layout", "box-sizing"]
        }
    ],
    "nextjs": [
        {
            "id": 1201,
            "question": "What is the benefit of Server-Side Rendering (SSR) in Next.js?",
            "ideal_answer": "SSR improves performance and SEO by pre-rendering pages on the server for each request. This ensures that search engines can easily crawl the content and users see the page faster.",
            "keywords": ["SEO", "performance", "pre-rendering", "server", "crawl", "getServerSideProps"]
        }
    ],
    "springboot": [
        {
            "id": 1301,
            "question": "What is Dependency Injection in Spring?",
            "ideal_answer": "Dependency Injection is a design pattern where the objects' dependencies are provided by the Spring container rather than the objects creating them themselves. This promotes loose coupling and easier testing.",
            "keywords": ["design pattern", "dependency", "coupling", "testing", "@Autowired", "IoC container"]
        }
    ],
    "system_design": [
        {
            "id": 1401,
            "question": "What is a Load Balancer and why is it used?",
            "ideal_answer": "A load balancer distributes incoming network traffic across multiple servers. This ensures no single server bears too much load, improving responsiveness and availability of the application.",
            "keywords": ["distributes", "traffic", "servers", "availability", "scalability", "redirect"]
        }
    ],
    "testing": [
        {
            "id": 1501,
            "question": "Difference between Unit Testing and Integration Testing?",
            "ideal_answer": "Unit testing tests individual components or functions in isolation. Integration testing tests how different modules or services work together as a group.",
            "keywords": ["isolation", "individual", "modules", "together", "group", "components"]
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
