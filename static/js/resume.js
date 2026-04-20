// ===============================
// DYNAMIC SECTION CONFIGURATION
// ===============================
const SECTION_TEMPLATES = {
    experience: {
        title: "Experience",
        html: `
            <div class="grid grid-2 gap-4 mb-4">
                <div class="input-group mb-0">
                    <label>Role / Position</label>
                    <input name="exp_role[]" placeholder="e.g. Software Engineer">
                </div>
                <div class="input-group mb-0">
                    <label>Company Name</label>
                    <input name="exp_company[]" placeholder="e.g. Google">
                </div>
            </div>
            <div class="grid grid-2 gap-4 mb-4 items-end">
                <div class="input-group mb-0">
                    <label>Start Date</label>
                    <input type="month" name="exp_start[]">
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
        `
    },
    projects: {
        title: "Projects",
        html: `
            <div class="grid grid-2 gap-4 mb-4">
                <div class="input-group mb-0">
                    <label>Project Name</label>
                    <input name="proj_name[]" placeholder="e.g. E-Commerce App">
                </div>
                <div class="input-group mb-0">
                    <label>Tech Stack</label>
                    <input name="proj_stack[]" placeholder="e.g. React, Node.js, MongoDB">
                </div>
            </div>
            <div class="input-group mb-0">
                <label>Project Description</label>
                <textarea name="proj_desc[]" rows="4" placeholder="Briefly describe what you built..."></textarea>
            </div>
        `
    },
    certifications: {
        title: "Certifications",
        html: `
            <div class="grid grid-2 gap-4">
                <div class="input-group mb-0">
                    <label>Certificate Name</label>
                    <input name="cert_name[]" placeholder="e.g. AWS Solutions Architect">
                </div>
                <div class="input-group mb-0">
                    <label>Issued By / Organization</label>
                    <input name="cert_org[]" placeholder="e.g. Amazon Web Services">
                </div>
            </div>
        `
    },
    achievements: {
        title: "Achievements",
        html: `
            <div class="grid grid-2 gap-4 mb-4">
                <div class="input-group mb-0">
                    <label>Achievement Title</label>
                    <input name="ach_title[]" placeholder="e.g. Winner of Smart India Hackathon">
                </div>
                <div class="input-group mb-0">
                    <label>Org / Event</label>
                    <input name="ach_org[]" placeholder="e.g. Govt of India">
                </div>
            </div>
            <div class="grid grid-2 gap-4">
                <div class="input-group mb-0">
                    <label>Date</label>
                    <input type="month" name="ach_date[]">
                </div>
                <div class="input-group mb-0">
                    <label>Brief Description</label>
                    <input name="ach_desc[]" placeholder="e.g. Ranked 1st among 500 teams">
                </div>
            </div>
        `
    },
    hobbies: {
        title: "Hobbies",
        html: `
            <div class="grid grid-2 gap-4">
                <div class="input-group mb-0">
                    <label>Hobby / Interest</label>
                    <input name="hobby_name[]" placeholder="e.g. Open Source Contribution">
                </div>
                <div class="input-group mb-0">
                    <label>Brief Description</label>
                    <input name="hobby_desc[]" placeholder="e.g. Active contributor to React ecosystem">
                </div>
            </div>
        `
    }
};

// ===============================
// CORE FUNCTIONS
// ===============================

function addItemToSection(slotNum) {
    const container = document.getElementById(`section-items-${slotNum}`);
    const sectionGroup = document.getElementById(`section-group-${slotNum}`);
    const type = sectionGroup.querySelector('.section-type-select').value;
    
    // Enforce 2 item limit
    if (container.children.length >= 2) {
        alert("You can only add up to 2 recent items in this section.");
        return;
    }

    const div = document.createElement("div");
    div.className = "card mb-4 p-6 relative";
    
    // Add remove button
    div.innerHTML = `
        <button type="button" onclick="this.parentElement.remove()" class="absolute top-2 right-2 text-muted hover:text-red-500" style="background: none; border: none; font-size: 1.2rem; cursor: pointer;">
            <i class="fas fa-times-circle"></i>
        </button>
        ${SECTION_TEMPLATES[type].html}
    `;

    container.appendChild(div);
}

function changeSectionType(slotNum, newType) {
    const container = document.getElementById(`section-items-${slotNum}`);
    
    // Confirm if they want to switch type (as it clears data)
    if (container.children.length > 0) {
        if (!confirm("Changing section type will clear current items in this slot. Continue?")) {
            // Revert select value
            const select = container.closest('.dynamic-section-group').querySelector('.section-type-select');
            // This is a bit tricky, but for now we just clear it if they proceed.
            return;
        }
    }
    
    container.innerHTML = "";
    addItemToSection(slotNum);
}

// ===============================
// EDUCATION (Separate as it's not interchangeable)
// ===============================
function addEducation() {
    const container = document.getElementById("education-container");
    if (container.children.length >= 2) {
        alert("You can only add up to 2 recent educations.");
        return;
    }

    const div = document.createElement("div");
    div.className = "card mb-4 p-6 relative";

    div.innerHTML = `
        <button type="button" onclick="this.parentElement.remove()" class="absolute top-2 right-2 text-muted hover:text-red-500" style="background: none; border: none; font-size: 1.2rem; cursor: pointer;">
            <i class="fas fa-times-circle"></i>
        </button>
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

function togglePresent(checkbox, endFieldName) {
    const parentContainer = checkbox.closest(".input-group");
    const endInput = parentContainer.querySelector(`input[name="${endFieldName}"]`);

    if (checkbox.checked) {
        endInput.value = "";
        endInput.disabled = true;
        endInput.style.backgroundColor = "#e2e8f0";
        endInput.style.opacity = "0.7";
        endInput.style.cursor = "not-allowed";
    } else {
        endInput.disabled = false;
        endInput.style.backgroundColor = "";
        endInput.style.opacity = "1";
        endInput.style.cursor = "text";
    }
}

// ===============================
// INITIALIZATION
// ===============================
document.addEventListener("DOMContentLoaded", () => {
    const edu = document.getElementById("education-container");
    if(edu && edu.children.length === 0) addEducation();

    // Init dynamic slots only if they are empty
    [1, 2, 3].forEach(slot => {
        const container = document.getElementById(`section-items-${slot}`);
        if(container && container.children.length === 0) {
            addItemToSection(slot);
        }
    });
});