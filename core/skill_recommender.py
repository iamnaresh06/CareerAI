SKILL_RECOMMENDATIONS = {
    "python": {
        "type": "Technical Skill",
        "recommendation": "Strengthen Python fundamentals, OOP concepts, and data structures.",
        "learning_path": "Basics → OOP → Data Structures → Projects"
    },
    "django": {
        "type": "Framework",
        "recommendation": "Learn Django models, views, templates, and REST APIs.",
        "learning_path": "MVT → ORM → Authentication → REST APIs"
    },
    "react": {
        "type": "Frontend",
        "recommendation": "Understand components, hooks, and state management.",
        "learning_path": "JSX → Hooks → State → Projects"
    },
    "sql": {
        "type": "Database",
        "recommendation": "Practice queries, joins, indexing, and normalization.",
        "learning_path": "Basic Queries → Joins → Optimization"
    },
    "aws": {
        "type": "Cloud",
        "recommendation": "Start with EC2, S3, IAM, and cloud basics.",
        "learning_path": "Cloud Basics → EC2 → Storage → Deployment"
    },
    "git": {
        "type": "Tool",
        "recommendation": "Learn version control, branching, and collaboration.",
        "learning_path": "Git Basics → Branching → GitHub"
    }
}

def generate_skill_guidance(missing_skills):
    guidance = []
    for skill in missing_skills:
        data = SKILL_RECOMMENDATIONS.get(skill.lower())
        if data:
            guidance.append({
                "skill": skill,
                "type": data["type"],
                "recommendation": data["recommendation"],
                "learning_path": data["learning_path"]
            })
        else:
            guidance.append({
                "skill": skill,
                "type": "General Skill",
                "recommendation": "Explore beginner to intermediate tutorials for this skill.",
                "learning_path": "Learn Basics → Than Practice → Make Projects"
            })
    return guidance