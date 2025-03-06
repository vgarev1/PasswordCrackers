document.addEventListener("DOMContentLoaded", function () {
    document.getElementById("passwordField").value = "test123";
});

async function copyToClipboard() {
    const passwordField = document.getElementById("passwordField");

    if (!passwordField.value) {
        alert("No password to copy!");
        return;
    }

    navigator.clipboard.writeText(passwordField.value).then(() => {
        const copyMessage = document.getElementById("copyMessage");
        copyMessage.innerText = "Password copied!";
        copyMessage.style.display = "block";

        setTimeout(() => {
            copyMessage.style.display = "none";
        }, 2000);
    }).catch(err => {
        console.error("Failed to copy password", err);
    });
}
