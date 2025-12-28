function addEducation() {
  document.getElementById("education-container").insertAdjacentHTML(
    "beforeend",
    `<div class="block">
      <input name="edu_degree[]" placeholder="Degree / Course">
      <input name="edu_college[]" placeholder="College Name">
      <input name="edu_start[]" type="month">
      <input name="edu_end[]" type="month">
      <input name="edu_score[]" placeholder="CGPA">
    </div>`
  );
}

function addExperience() {
  document.getElementById("experience-container").insertAdjacentHTML(
    "beforeend",
    `<div class="block">
      <input name="exp_role[]" placeholder="Role">
      <input name="exp_company[]" placeholder="Company">
      <input name="exp_start[]" type="month">
      <input name="exp_end[]" placeholder="End / Present">
      <textarea name="exp_desc[]" placeholder="Description"></textarea>
    </div>`
  );
}

function addProject() {
  document.getElementById("project-container").insertAdjacentHTML(
    "beforeend",
    `<div class="block">
      <input name="proj_name[]" placeholder="Project Name">
      <input name="proj_stack[]" placeholder="Tech Stack">
      <textarea name="proj_desc[]" placeholder="Description"></textarea>
    </div>`
  );
}

function addCertification() {
  document.getElementById("certification-container").insertAdjacentHTML(
    "beforeend",
    `<div class="block">
      <input name="cert_name[]" placeholder="Certificate Name">
      <input name="cert_org[]" placeholder="Issued By">
    </div>`
  );
}

window.onload = () => {
  addEducation();
  addExperience();
  addProject();
  addCertification();
};

const skillSuggestions = [
  "Python", "Java", "C", "C++",
  "HTML", "CSS", "JavaScript", "Django",
  "SQL", "DBMS", "Computer Networks",
  "Data Structures", "Algorithms",
  "Git", "Docker", "Machine Learning"
];

document.addEventListener("input", function (e) {
  if (e.target.name === "skills") {
    let value = e.target.value.toLowerCase();
    let match = skillSuggestions.find(s =>
      s.toLowerCase().startsWith(value.split(",").pop().trim())
    );
    if (match) {
      e.target.setAttribute("list", "skills-list");
    }
  }
});
