document.addEventListener("DOMContentLoaded", function () {
    const yearSpan = document.getElementById("copyright-year");
    const currentYear = new Date().getFullYear();
    if (yearSpan) {
        yearSpan.textContent = currentYear;
    }
    if (currentYear > 2025) {
        yearSpan.textContent = "2025" + "-" + new Date().getFullYear();
    }
});