// ===============================
// EDUCATION
// ===============================
function addEducation() {
    const container = document.getElementById("education-container");

    const div = document.createElement("div");
    div.className = "card glass mb-4 p-6"; // Increased padding

    div.innerHTML = `
        <div class="grid grid-2 gap-4 mb-4">
            <div class="input-group mb-0">
                <label>Degree</label>
                <input name="edu_degree[]" placeholder="e.g. B.Tech Computer Science" required>
            </div>
            <div class="input-group mb-0">
                <label>College / University</label>
                <input name="edu_college[]" placeholder="e.g. IIT Madras" required>
            </div>
        </div>

        <div class="grid grid-2 gap-4 mb-4 items-end">
            <div class="input-group mb-0">
                <label>Start Date</label>
                <input type="month" name="edu_start[]" required>
            </div>
            <div class="input-group mb-0">
                <label>End Date</label>
                <div class="flex gap-2 items-center">
                    <input type="month" name="edu_end[]" style="flex: 1;">
                    <label class="flex items-center gap-1" style="white-space: nowrap; cursor: pointer; margin-bottom: 0;">
                        <input type="checkbox" onchange="togglePresent(this, 'edu_end[]')" style="width: auto;">
                        <span>Present</span>
                    </label>
                </div>
            </div>
        </div>

        <div class="input-group mb-0">
            <label>Score (CGPA/%)</label>
            <input name="edu_score[]" placeholder="e.g. 8.5">
        </div>
    `;

    container.appendChild(div);
}


// ===============================
// EXPERIENCE
// ===============================
function addExperience() {
    const container = document.getElementById("experience-container");

    const div = document.createElement("div");
    div.className = "card glass mb-4 p-6";

    div.innerHTML = `
        <div class="grid grid-2 gap-4 mb-4">
            <div class="input-group mb-0">
                <label>Role / Position</label>
                <input name="exp_role[]" placeholder="e.g. Software Engineer" required>
            </div>
            <div class="input-group mb-0">
                <label>Company Name</label>
                <input name="exp_company[]" placeholder="e.g. Google" required>
            </div>
        </div>

        <div class="grid grid-2 gap-4 mb-4 items-end">
            <div class="input-group mb-0">
                <label>Start Date</label>
                <input type="month" name="exp_start[]" required>
            </div>
            <div class="input-group mb-0">
                <label>End Date</label>
                <div class="flex gap-2 items-center">
                    <input type="month" name="exp_end[]" style="flex: 1;">
                    <label class="flex items-center gap-1" style="white-space: nowrap; cursor: pointer; margin-bottom: 0;">
                        <input type="checkbox" onchange="togglePresent(this, 'exp_end[]')" style="width: auto;">
                        <span>Present</span>
                    </label>
                </div>
            </div>
        </div>

        <div class="input-group mb-0">
            <label>Work Description (MAX 3 points, separate by new lines)</label>
            <textarea name="exp_desc[]" rows="4" placeholder="Developed ...&#10;Collaborated ..."></textarea>
        </div>
    `;

    container.appendChild(div);
}


// ===============================
// PROJECTS
// ===============================
function addProject() {
    const container = document.getElementById("projects-container");

    const div = document.createElement("div");
    div.className = "card glass mb-4 p-6";

    div.innerHTML = `
        <div class="grid grid-2 gap-4 mb-4">
            <div class="input-group mb-0">
                <label>Project Name</label>
                <input name="proj_name[]" placeholder="e.g. E-Commerce App" required>
            </div>
            <div class="input-group mb-0">
                <label>Tech Stack</label>
                <input name="proj_stack[]" placeholder="e.g. React, Node.js, MongoDB" required>
            </div>
        </div>
        <div class="input-group mb-0">
            <label>Project Description</label>
            <textarea name="proj_desc[]" rows="4" placeholder="Briefly describe what you built..."></textarea>
        </div>
    `;

    container.appendChild(div);
}


// ===============================
// CERTIFICATIONS
// ===============================
function addCertification() {
    const container = document.getElementById("certifications-container");

    const div = document.createElement("div");
    div.className = "card glass mb-4 p-6";

    div.innerHTML = `
        <div class="grid grid-2 gap-4">
            <div class="input-group mb-0">
                <label>Certificate Name</label>
                <input name="cert_name[]" placeholder="e.g. AWS Solutions Architect" required>
            </div>
            <div class="input-group mb-0">
                <label>Issued By / Organization</label>
                <input name="cert_org[]" placeholder="e.g. Amazon Web Services" required>
            </div>
        </div>
    `;

    container.appendChild(div);
}


// ===============================
// PRESENT TOGGLE (CORE LOGIC)
// ===============================
function togglePresent(checkbox, endFieldName) {
    const parentContainer = checkbox.closest(".flex");
    const endInput = parentContainer.querySelector(`input[name="${endFieldName}"]`);

    if (checkbox.checked) {
        endInput.value = "";
        endInput.disabled = true;
        endInput.style.opacity = "0.5";
        endInput.style.pointerEvents = "none";
    } else {
        endInput.disabled = false;
        endInput.style.opacity = "1";
        endInput.style.pointerEvents = "auto";
    }
}


// ===============================
// AUTO ADD FIRST BLOCKS
// ===============================
document.addEventListener("DOMContentLoaded", () => {
    const edu = document.getElementById("education-container");
    const exp = document.getElementById("experience-container");
    const prj = document.getElementById("projects-container");
    const cert = document.getElementById("certifications-container");

    if(edu && edu.children.length === 0) addEducation();
    if(exp && exp.children.length === 0) addExperience();
    if(prj && prj.children.length === 0) addProject();
    if(cert && cert.children.length === 0) addCertification();
});