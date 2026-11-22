// TAMS basic validation handlers. No libraries or global shared dependency.
function handleFieldChange(event) {
    validateField(event.target);
}

// validate Field
function validateField(field) {
    field.setCustomValidity("");
    if (field.disabled || field.type === "hidden" || field.type === "button" || field.type === "submit") return true;
    const value = field.value.trim();
    let error = "";
    // Check for required input, email, number, telephone number
    if (field.required && (field.type === "checkbox" ? !field.checked : !value)) {
        error = "This field is required.";
    } else if (value && field.type === "email" && !/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(value)) {
        error = "Enter a valid email address.";
    } else if (value && field.type === "number" && !field.validity.valid) {
        error = "Enter a number within the allowed range.";
    } else if (value && field.type === "tel" && !/^[+()0-9 .-]{7,20}$/.test(value)) {
        error = "Enter a valid phone number.";
    } else if (value && !field.validity.valid) {
        error = field.validationMessage || "Check this field.";
    }
    field.setCustomValidity(error);
    return error === "";
}

function validateRelatedFields(form) {
    let valid = true;
    const datePairs = [["start_date", "end_date"], ["date_from", "date_to"], ["period_start", "period_end"]];
    datePairs.forEach(function (pair) {
        const start = form.elements.namedItem(pair[0]);
        const end = form.elements.namedItem(pair[1]);
        if (!start || !end) return;
        const error = start.value && end.value && end.value < start.value
            ? "End date cannot be before start date." : "";
        end.setCustomValidity(error);
        if (error) valid = false;
    });

    const password = form.elements.namedItem("new_password");
    const confirmation = form.elements.namedItem("confirm_password");
    if (password && confirmation) {
        const error = password.value !== confirmation.value ? "Passwords do not match." : "";
        confirmation.setCustomValidity(error);
        if (error) valid = false;
    }

    // Admin: changing an account status requires a reason.
    if (document.body.dataset.page === "account_status_management") {
        const reason = form.elements.namedItem("reason");
        if (reason) {
            const error = reason.value.trim() ? "" : "Please provide a reason.";
            reason.setCustomValidity(error);
            if (error) valid = false;
        }
    }
    return valid;
}

function handleFormSubmit(event) {
    const form = event.currentTarget;
    let valid = true;
    form.querySelectorAll("input, select, textarea").forEach(function (field) {
        if (!validateField(field)) valid = false;
    });
    if (!validateRelatedFields(form)) valid = false;

    if (!valid) {
        event.preventDefault();
        form.reportValidity();
        console.log("TAMS: validation failed");
        return;
    }

    if (document.body.dataset.page === "account_status_management") {
        if (!confirm("Are you sure you want to change this account status?")) {
            event.preventDefault();
            return;
        }
    }

    // Standalone HTML demo: do not POST to a missing backend.
    // Remove this demo block once Django form actions are connected.
    if (!form.getAttribute("action")) {
        event.preventDefault();
        console.log("TAMS: validation passed (demo only)");
        alert("Validation successful! Backend submission is not connected yet.");
    }
}
