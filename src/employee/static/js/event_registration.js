// Register events for forms belonging to this application.
document.addEventListener("DOMContentLoaded", function () {
    const forms = document.querySelectorAll("form");
    console.log("TAMS validation loaded:", document.body.dataset.page, forms.length, "form(s)");

    forms.forEach(function (form) {
        // Our submit handler checks empty fields too (instead of native validation blocking it).
        form.noValidate = true;
        form.addEventListener("submit", handleFormSubmit);
        form.querySelectorAll("input, select, textarea").forEach(function (field) {
            field.addEventListener("blur", handleFieldChange);
            field.addEventListener("change", handleFieldChange);
            field.addEventListener("input", handleFieldChange);
        });
    });
});
