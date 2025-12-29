// ===============================
// EDUCATION
// ===============================
function addEducation() {
    const container = document.getElementById("education-container");

    const div = document.createElement("div");
    div.className = "block";

    div.innerHTML = `
        <input name="edu_degree[]" placeholder="Degree (e.g. MCA)">
        <input name="edu_college[]" placeholder="College / University">

        <div class="row">
            <input type="month" name="edu_start[]">
            <input type="month" name="edu_end[]">
            <label class="present-label">
                <input type="checkbox" onchange="togglePresent(this, 'edu_end[]')">
                Present
            </label>
        </div>

        <input name="edu_score[]" placeholder="CGPA / Percentage">
        <hr>
    `;

    container.appendChild(div);
}


// ===============================
// EXPERIENCE
// ===============================
function addExperience() {
    const container = document.getElementById("experience-container");

    const div = document.createElement("div");
    div.className = "block";

    div.innerHTML = `
        <input name="exp_role[]" placeholder="Role (e.g. Python Developer Intern)">
        <input name="exp_company[]" placeholder="Company Name">

        <div class="row">
            <input type="month" name="exp_start[]">
            <input type="month" name="exp_end[]">
            <label class="present-label">
                <input type="checkbox" onchange="togglePresent(this, 'exp_end[]')">Present
            </label>
        </div>

        <textarea name="exp_desc[]" placeholder="EXPERIENCE DESCRIPTION - Please Follow The Below Format
Enter each point on a new line - (MAX 3 points)"></textarea>
        <hr>
    `;

    container.appendChild(div);
}


// ===============================
// PROJECTS
// ===============================
function addProject() {
    const container = document.getElementById("projects-container");

    const div = document.createElement("div");
    div.className = "block";

    div.innerHTML = `
        <input name="proj_name[]" placeholder="Project Name">
        <input name="proj_stack[]" placeholder="Tech Stack (Python, Django, MySQL)">
        <textarea name="proj_desc[]" placeholder="PROJECT DESCRIPTION - Please Follow The Below Format
Enter each point on a new line - (MAX 3 points)"></textarea>
        <hr>
    `;

    container.appendChild(div);
}


// ===============================
// CERTIFICATIONS
// ===============================
function addCertification() {
    const container = document.getElementById("certifications-container");

    const div = document.createElement("div");
    div.className = "block";

    div.innerHTML = `
        <input name="cert_name[]" placeholder="Certificate Name">
        <input name="cert_org[]" placeholder="Issued By">
        <hr>
    `;

    container.appendChild(div);
}


// ===============================
// PRESENT TOGGLE (CORE LOGIC)
// ===============================
function togglePresent(checkbox, endFieldName) {
    const parent = checkbox.closest(".row");
    const endInput = parent.querySelector(`input[name="${endFieldName}"]`);

    if (checkbox.checked) {
        endInput.value = "";
        endInput.disabled = true;
        endInput.placeholder = "Present";
    } else {
        endInput.disabled = false;
        endInput.placeholder = "";
    }
}


// ===============================
// AUTO ADD FIRST BLOCKS
// ===============================
document.addEventListener("DOMContentLoaded", () => {
    addEducation();
    addExperience();
    addProject();
    addCertification();
});