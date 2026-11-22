// Register events for forms 
// Working --- ----
// Get all the forms in the application
// Validate the input for each form
document.addEventListener("DOMContentLoaded", function () {
    const forms = document.querySelectorAll("form");
    console.log("TAMS validation loaded:", document.body.dataset.page, forms.length, "form(s)");

    forms.forEach(function (form) {

        form.noValidate = true;
        form.addEventListener("submit", handleFormSubmit);
        form.querySelectorAll("input, select, textarea").forEach(function (field) {
            field.addEventListener("blur", handleFieldChange);
            field.addEventListener("change", handleFieldChange);
            field.addEventListener("input", handleFieldChange);
        });
    });
});
