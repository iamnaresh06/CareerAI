"""
Career Advisor Engine for CareerAI.

This module provides high-level career guidance, including:
1. Job Readiness Scoring (based on resume & skill analysis).
2. Action Plan Generation for students to improve their employability.
3. Career Roadmap suggestions based on current profile.

Usage:
    - Called after Resume Analysis to provide next steps.
    - Used in the Job Readiness Dashboard.

Author: Naresh Reddy
"""

def calculate_readiness_score(resume_score, skill_score, missing_skills_count):
    """
    Computes a 'Job Readiness' score (0-100) tailored for freshers.
    
    The score is more lenient than strict ATS matching to encourage students,
    while still providing a realistic assessment of their preparedness.
    
    Args:
        resume_score (float): The ML-based resume match percentage.
        skill_score (float): The skill-specific match percentage.
        missing_skills_count (int): Number of critical skills missing.
        
    Returns:
        int: A rounded score representing job readiness.
    """
    # Defensive programming against None
    resume_score = float(resume_score or 0)
    skill_score = float(skill_score or 0)

    # Base score to prevent demotivation (never show 0%)
    base_score = 20

    # Core calculation: Average of resume and skill match
    average_performance = (resume_score + skill_score) / 2
    
    # Calculate initial readiness
    readiness = base_score + int(average_performance)

    # Apply penalty for missing critical skills
    # Caps penalty at 20 points max
    penalty = min(missing_skills_count * 3, 20)
    
    readiness -= penalty

    # Clamp result between 20 (min) and 100 (max)
    readiness = max(20, min(readiness, 100))

    return readiness


def generate_action_plan(missing_skills):
    """
    Creates a step-by-step action plan for the student.
    
    Args:
        missing_skills (list): List of improved areas.
        
    Returns:
        list: A list of actionable strings.
    """
    plan = []

    # Step 1: Foundation
    plan.append("Revise core CS fundamentals (Data Structures & Algos) which are crucial for interviews.")

    # Step 2: Skill Gap
    if missing_skills:
        # Show top 3 missing skills to focus on
        top_missing = missing_skills[:3]
        skills_str = ", ".join(top_missing)
        plan.append(f"Prioritize learning these missing skills: {skills_str}.")
    else:
        plan.append("Your skill set looks strong! Focus on advanced concepts and system design.")

    # Step 3: Practical Application
    plan.append("Build at least one end-to-end full-stack project and deploy it.")

    # Step 4: Interview Prep
    plan.append("Practice mock interviews and behavioral questions (STAR method).")
    
    return plan
