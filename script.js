// script.js
document.getElementById("submit-form").addEventListener("click", function () {
    const age = document.getElementById("age").value;
    const smoking = document.getElementById("smoking").value;
    const diabetes = document.getElementById("diabetes").value;

    let riskStatus = "No Risk";

    if (age > 40 || smoking === "yes" || diabetes === "yes") {
        riskStatus = "At Risk";
    }

    document.getElementById("form-section").style.display = "none";
    document.getElementById("result-section").style.display = "block";
    document.getElementById("risk-status").textContent = `Your health risk status is: ${riskStatus}`;
});

document.getElementById("book-appointment").addEventListener("click", function () {
    document.getElementById("result-section").style.display = "none";
    document.getElementById("appointment-section").style.display = "block";
});

document.getElementById("confirm-appointment").addEventListener("click", function () {
    alert("Your appointment has been confirmed!");
});

