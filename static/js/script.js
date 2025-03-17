function showUploadOption() {
    let imageUpload = document.getElementById("imageUpload");
    let textInput = document.getElementById("textInput");

    imageUpload.classList.add("show");
    textInput.classList.remove("show");

    // Reset text input when switching to file upload
    textInput.value = "";
}

function showTextOption() {
    let imageUpload = document.getElementById("imageUpload");
    let textInput = document.getElementById("textInput");

    textInput.classList.add("show");
    imageUpload.classList.remove("show");

    // Reset file input when switching to text
    imageUpload.value = "";
}

async function submitData() {
    const selectedLanguage = document.getElementById("languageSelect").value;
    const imageUpload = document.getElementById("imageUpload");
    const textInput = document.getElementById("textInput");

    const formData = new FormData();
    formData.append("language", selectedLanguage);

    // Check if an image is uploaded
    if (imageUpload.classList.contains("show") && imageUpload.files.length > 0) {
        formData.append("image", imageUpload.files[0]);
    } 
    // Check if text is provided
    else if (textInput.classList.contains("show") && textInput.value.trim() !== "") {
        formData.append("text", textInput.value.trim());
    } 
    // If neither is provided
    else {
        alert("Please provide either text or an image.");
        return;
    }

    try {
        const response = await fetch("/process_image", {
            method: "POST",
            body: formData
        });

        if (!response.ok) {
            throw new Error("Network response was not ok");
        }

        const data = await response.json();

        if (data.error) {
            alert("Error: " + data.error);
            return;
        }

        // Display results
        document.getElementById("results").classList.remove("hidden");
        document.getElementById("originalText").textContent = data.original_text || "No original text found.";
        document.getElementById("translatedText").textContent = data.translated_text || "No translated text available.";
    } catch (error) {
        alert("Error: " + error.message);
    }
}
