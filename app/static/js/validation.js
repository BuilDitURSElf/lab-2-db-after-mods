// [R8] Browser-side checks. The server repeats the same rules (app/validators.py).
// Rules are read from data-* attributes written in the templates.

// Returns the error message for one input, or "" when it is fine.
function checkInput(form, input) {
  const value = input.value;
  // passwords are not trimmed (spaces can be part of a password); other fields are
  const isEmpty = input.type === "password" ? value === "" : value.trim() === "";

  if (isEmpty) return input.dataset.required;

  if (input.dataset.max && value.trim().length > Number(input.dataset.max)) {
    return input.dataset.maxMsg;
  }
  if (input.dataset.match) {
    const other = form.querySelector('[name="' + input.dataset.match + '"]');
    if (other && value !== other.value) return input.dataset.matchMsg;
  }
  return "";
}

// Writes the message in the red text under the field (or clears it).
function showError(form, input, message) {
  const holder = input.closest(".field") || form;
  holder.querySelector(".error").textContent = message;
  input.classList.toggle("invalid", message !== "");
}

// Checks every input of a form. Returns true when all are fine.
function validateForm(form) {
  let allGood = true;
  form.querySelectorAll("input[data-required]").forEach(function (input) {
    const message = checkInput(form, input);
    showError(form, input, message);
    if (message !== "") allGood = false;
  });
  return allGood;
}

document.addEventListener("DOMContentLoaded", function () {
  // Forms with data-validate: stop the submit when something is wrong (nothing is sent).
  document.querySelectorAll("form[data-validate]").forEach(function (form) {
    form.addEventListener("submit", function (event) {
      if (!validateForm(form)) event.preventDefault();
    });
    // remove the message while the user fixes the field
    form.querySelectorAll("input[data-required]").forEach(function (input) {
      input.addEventListener("input", function () {
        showError(form, input, "");
      });
    });
  });

  // [R7] Forms with data-confirm: ask "are you sure?" before sending.
  document.querySelectorAll("form[data-confirm]").forEach(function (form) {
    form.addEventListener("submit", function (event) {
      if (!window.confirm(form.dataset.confirm)) event.preventDefault();
    });
  });
});
