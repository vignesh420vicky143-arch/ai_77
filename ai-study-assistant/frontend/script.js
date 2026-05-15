const API_BASE = 'http://127.0.0.1:5000';

//
// Upload PDF
//
async function uploadPDF() {

    const fileInput =
        document.getElementById('pdfFile');

    // Check file selected
    if (!fileInput.files[0]) {

        alert("Please select a PDF file");

        return;
    }

    // Check PDF type
    const file = fileInput.files[0];

    if (file.type !== "application/pdf") {

        document.getElementById('output')
            .innerText =
            "Please upload only PDF files.";

        return;
    }

    const formData = new FormData();

    formData.append('file', file);

    try {

        document.getElementById('output')
            .innerText = "Uploading PDF...";

        const response = await fetch(
            `${API_BASE}/upload`,
            {
                method: 'POST',
                body: formData
            }
        );

        const data = await response.json();

        if (data.error) {

            document.getElementById('output')
                .innerText = data.error;

            return;
        }

        document.getElementById('output')
            .innerText =
            `PDF Uploaded Successfully

Characters Extracted: ${data.characters}`;

    } catch (error) {

        document.getElementById('output')
            .innerText =
            "Server Error: " + error;
    }
}

//
// Ask Question
//
async function askQuestion() {

    const question =
        document.getElementById('question').value;

    if (!question) {

        alert("Please enter a question");

        return;
    }

    try {

        document.getElementById('output')
            .innerText = "AI is thinking...";

        const response = await fetch(
            `${API_BASE}/ask`,
            {
                method: 'POST',

                headers: {
                    'Content-Type': 'application/json'
                },

                body: JSON.stringify({
                    question: question
                })
            }
        );

        const data = await response.json();

        if (data.error) {

            document.getElementById('output')
                .innerText = data.error;

            return;
        }

        document.getElementById('output')
            .innerText = data.answer;

    } catch (error) {

        document.getElementById('output')
            .innerText =
            "Server Error: " + error;
    }
}

//
// Generate Summary
//
async function getSummary() {

    try {

        document.getElementById('output')
            .innerText = "Generating summary...";

        const response = await fetch(
            `${API_BASE}/summary`
        );

        const data = await response.json();

        if (data.error) {

            document.getElementById('output')
                .innerText = data.error;

            return;
        }

        document.getElementById('output')
            .innerText = data.summary;

    } catch (error) {

        document.getElementById('output')
            .innerText =
            "Server Error: " + error;
    }
}