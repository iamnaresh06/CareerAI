def generate_feedback(final_score, skill_score, missing_skills):
    final_score = float(final_score)
    skill_score = float(skill_score)

    # smarter feedback logic
    if final_score >= 75 or (final_score >= 70 and skill_score >= 60):
        message = (
            "Strong match. Your resume aligns well with the job requirements."
        )
    elif final_score >= 50:
        message = (
            "Good match. Your resume meets most of the job requirements, "
            "but a few improvements can increase your chances."
        )
    else:
        message = (
            "Low match. Your resume does not strongly align with the job requirements. "
            "Consider improving the highlighted skills."
        )

    if missing_skills:
        skills_text = ", ".join(missing_skills)
        message += f" Missing skills include {skills_text}."

    return message