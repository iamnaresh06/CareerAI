def calculate_job_readiness(resume_score, skill_score, missing_skills):
    """
    Calculates job readiness score in a fresher-friendly way
    """

    # Ensure safe defaults
    resume_score = resume_score or 0
    skill_score = skill_score or 0

    # Base score so freshers never see 0%
    BASE_SCORE = 20

    # Core calculation
    readiness = BASE_SCORE + int((resume_score + skill_score) / 2)

    # Penalize gently for missing skills
    penalty = min(len(missing_skills) * 3, 20)
    readiness -= penalty

    # Clamp between 20 and 100
    readiness = max(20, min(readiness, 100))

    return readiness


def generate_action_plan(missing_skills):
    plan = []

    plan.append("Revise core fundamentals and basics related to your field.")

    if missing_skills:
        plan.append("Focus on learning these missing skills: " + ", ".join(missing_skills))
    else:
        plan.append("Strengthen existing skills by building small projects.")

    plan.append("Build at least one practical project and upload it to GitHub.")
    plan.append("Practice interview questions and revise weak areas.")

    return plan