// ===============================
// GLOBAL VARIABLE
// ===============================
let selectedFile = null;

// ===============================
// ELEMENTS
// ===============================
const dropArea = document.getElementById("drop-area");
const fileInput = document.getElementById("fileElem");
const preview = document.getElementById("preview");
const detectBtn = document.getElementById("detectBtn");
const chooseBtn = document.getElementById("chooseBtn");

const loading = document.getElementById("loading");
const resultBox = document.getElementById("resultBox");
const result = document.getElementById("result");
const errorBox = document.getElementById("errorBox");
const errorText = document.getElementById("errorText");

// ===============================
// OPEN FILE PICKER
// ===============================
chooseBtn.addEventListener("click", () => {
    fileInput.click();
});

// ===============================
// FILE INPUT CHANGE
// ===============================
fileInput.addEventListener("change", handleFiles);

// ===============================
// DRAG EVENTS
// ===============================
dropArea.addEventListener("dragover", (e) => {
    e.preventDefault();
    dropArea.classList.add("dragover");
});

dropArea.addEventListener("dragleave", () => {
    dropArea.classList.remove("dragover");
});

dropArea.addEventListener("drop", (e) => {
    e.preventDefault();
    dropArea.classList.remove("dragover");

    if (e.dataTransfer.files.length > 0) {
        fileInput.files = e.dataTransfer.files;
        handleFiles();
    }
});

// ===============================
// HANDLE FILE
// ===============================
function handleFiles() {
    selectedFile = fileInput.files[0];

    if (!selectedFile) return;

    // Show preview
    const reader = new FileReader();
    reader.onload = function(e) {
        preview.src = e.target.result;
        preview.style.display = "block";
    };
    reader.readAsDataURL(selectedFile);

    // Enable detect button
    detectBtn.disabled = false;

    // Hide old results/errors
    resultBox.style.display = "none";
    errorBox.style.display = "none";
}

// ===============================
// DETECT BUTTON CLICK
// ===============================
detectBtn.addEventListener("click", uploadImage);

// ===============================
// UPLOAD IMAGE
// ===============================
function uploadImage() {
    if (!selectedFile) {
        showError("Please select an image first.");
        return;
    }

    const formData = new FormData();
    formData.append("image", selectedFile);

    loading.style.display = "block";
    resultBox.style.display = "none";
    errorBox.style.display = "none";

    fetch("/predict_disease", {
        method: "POST",
        body: formData
    })
    .then(response => response.json())
    .then(data => {
        loading.style.display = "none";

        if (data.error) {
            showError(data.error);
        } else {
            result.innerHTML = `
    <strong>Disease:</strong> ${data.disease}
    <br><br>

    <strong>Solution:</strong> ${data.solution}
`;
            resultBox.style.display = "block";
        }
    })
    .catch(error => {
        loading.style.display = "none";
        showError("Something went wrong.");
        console.error(error);
    });
}

// ===============================
// SHOW ERROR
// ===============================
function showError(msg) {
    errorText.innerText = msg;
    errorBox.style.display = "block";
}