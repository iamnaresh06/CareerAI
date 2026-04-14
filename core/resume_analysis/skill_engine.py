"""
Skill Analysis & Guidance Engine for CareerAI.

This module provides tailored recommendations and learning paths for specific
technical skills identified as 'missing' from a student's profile.

Knowledge Base:
    - Programming Languages
    - Frameworks
    - Cloud Platforms
    - Tools

Author: Naresh Reddy
"""

# Knowledge Base: Hardcoded for simplicity but extensible
SKILL_RECOMMENDATIONS = {
    # Programming Languages
    "python": {
        "type": "Technical Skill",
        "recommendation": "Strengthen Python fundamentals, OOP concepts, and data structures.",
        "learning_path": "Basics → OOP → Data Structures → Projects"
    },
    "java": {
        "type": "Programming Language",
        "recommendation": "Focus on Core Java, OOPs, Collections framework, and Multithreading.",
        "learning_path": "Syntax → OOPs → Java 8 Features → JDBC"
    },
    "javascript": {
        "type": "Frontend Language",
        "recommendation": "Master ES6 features, DOM manipulation, and asynchronous programming.",
        "learning_path": "JS Basics → ES6+ → Async/Await → API Fetching"
    },
    
    # Frameworks
    "django": {
        "type": "Web Framework",
        "recommendation": "Learn Django models, views, templates, and REST APIs.",
        "learning_path": "MVT → ORM → Authentication → REST APIs"
    },
    "react": {
        "type": "Frontend Library",
        "recommendation": "Understand components, hooks, and state management.",
        "learning_path": "JSX → Hooks → State → Redux"
    },
    
    # Databases
    "sql": {
        "type": "Database",
        "recommendation": "Practice queries, joins, indexing, and normalization.",
        "learning_path": "Basic Queries → Joins → Optimization"
    },
    
    # Cloud & DevOps
    "aws": {
        "type": "Cloud Platform",
        "recommendation": "Start with EC2, S3, IAM, and cloud basics.",
        "learning_path": "Cloud Basics → EC2 → Storage → Deployment"
    },
    "git": {
        "type": "Version Control",
        "recommendation": "Learn version control, branching, and collaboration.",
        "learning_path": "Git Basics → Branching → GitHub"
    }
}


def generate_skill_guidance(missing_skills):
    """
    Generates actionable advice for a list of missing skills.
    
    Args:
        missing_skills (list): A list of skill names (strings).
        
    Returns:
        list: A list of dicts containing advice for each skill.
    """
    guidance = []
    
    for skill in missing_skills:
        # Normalize skill name for lookup
        normalized_skill = skill.lower()
        
        data = SKILL_RECOMMENDATIONS.get(normalized_skill)
        
        if data:
            guidance.append({
                "skill": skill,
                "type": data["type"],
                "recommendation": data["recommendation"],
                "learning_path": data["learning_path"]
            })
        else:
            # Fallback for unknown skills
            guidance.append({
                "skill": skill,
                "type": "General Skill",
                "recommendation": f"Explore beginner to intermediate tutorials for {skill}.",
                "learning_path": "Learn Basics → Practice -> Build Projects"
            })
            
    return guidance
