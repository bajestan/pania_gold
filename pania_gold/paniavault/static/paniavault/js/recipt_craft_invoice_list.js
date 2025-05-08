
document.addEventListener("DOMContentLoaded", function () {
    const icons = document.querySelectorAll(".details-icon");
    icons.forEach(icon => {
        icon.addEventListener("click", function () {
            const invoiceId = this.getAttribute("data-invoice-id");
            const detailsRow = document.getElementById(`details-${invoiceId}`);
            if (detailsRow.style.display === "none") {
                detailsRow.style.display = "table-row";
            } else {
                detailsRow.style.display = "none";
            }
        });
    });
});
