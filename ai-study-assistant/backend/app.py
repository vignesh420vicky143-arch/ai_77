from flask import Flask, request, jsonify
from flask_cors import CORS
from PyPDF2 import PdfReader
from openai import OpenAI
from dotenv import load_dotenv
import os

# -----------------------------------
# Load Environment Variables
# -----------------------------------
load_dotenv()

# -----------------------------------
# OpenAI API Key
# -----------------------------------
api_key = os.getenv("OPENAI_API_KEY")

if not api_key:
    raise ValueError(
        "OPENAI_API_KEY not found in .env file"
    )

# -----------------------------------
# OpenAI Client
# -----------------------------------
client = OpenAI(api_key=api_key)

# -----------------------------------
# Flask App
# -----------------------------------
app = Flask(__name__)
CORS(app)

# -----------------------------------
# Upload Folder Setup
# -----------------------------------
BASE_DIR = os.path.dirname(
    os.path.abspath(__file__)
)

UPLOAD_FOLDER = os.path.join(
    BASE_DIR,
    "uploads"
)

# Create uploads folder safely
os.makedirs(
    UPLOAD_FOLDER,
    exist_ok=True
)

# -----------------------------------
# Store PDF Text Temporarily
# -----------------------------------
pdf_text_store = ""

# -----------------------------------
# Home Route
# -----------------------------------
@app.route('/')
def home():

    return "AI Study Assistant Backend Running"

# -----------------------------------
# Upload PDF API
# -----------------------------------
@app.route('/upload', methods=['POST'])
def upload_pdf():

    global pdf_text_store

    try:

        # Check file
        if 'file' not in request.files:

            return jsonify({
                "error": "No file uploaded"
            }), 400

        file = request.files['file']

        # Empty filename check
        if file.filename == '':

            return jsonify({
                "error": "No selected file"
            }), 400

        # Create full file path
        filepath = os.path.join(
            UPLOAD_FOLDER,
            file.filename
        )

        # Save file
        file.save(filepath)

        # Read PDF
        reader = PdfReader(filepath)

        text = ""

        # Extract text from pages
        for page in reader.pages:

            extracted = page.extract_text()

            if extracted:
                text += extracted

        # Store extracted text
        pdf_text_store = text

        return jsonify({
            "message": "PDF Uploaded Successfully",
            "characters": len(text)
        })

    except Exception as e:

        return jsonify({
            "error": str(e)
        }), 500

# -----------------------------------
# Ask Question API
# -----------------------------------
@app.route('/ask', methods=['POST'])
def ask_question():

    global pdf_text_store

    try:

        # Check PDF uploaded
        if not pdf_text_store:

            return jsonify({
                "error": "Please upload PDF first"
            }), 400

        # Get JSON data
        data = request.get_json()

        if not data:

            return jsonify({
                "error": "No data received"
            }), 400

        # Get question
        question = data.get('question')

        if not question:

            return jsonify({
                "error": "Question is required"
            }), 400

        # Create AI prompt
        prompt = f"""
You are an AI Study Assistant.

Study Material:
{pdf_text_store[:12000]}

Student Question:
{question}

Give a clear and simple educational answer.
"""

        # OpenAI API call
        response = client.chat.completions.create(

            model="gpt-4.1-mini",

            messages=[
                {
                    "role": "user",
                    "content": prompt
                }
            ]
        )

        # Extract answer
        answer = response.choices[0].message.content

        return jsonify({
            "answer": answer
        })

    except Exception as e:

        return jsonify({
            "error": str(e)
        }), 500

# -----------------------------------
# Summary API
# -----------------------------------
@app.route('/summary', methods=['GET'])
def generate_summary():

    global pdf_text_store

    try:

        # Check PDF uploaded
        if not pdf_text_store:

            return jsonify({
                "error": "Please upload PDF first"
            }), 400

        # Create summary prompt
        prompt = f"""
Summarize the following study material into simple bullet points:

{pdf_text_store[:12000]}
"""

        # OpenAI API call
        response = client.chat.completions.create(

            model="gpt-4.1-mini",

            messages=[
                {
                    "role": "user",
                    "content": prompt
                }
            ]
        )

        # Extract summary
        summary = response.choices[0].message.content

        return jsonify({
            "summary": summary
        })

    except Exception as e:

        return jsonify({
            "error": str(e)
        }), 500

# -----------------------------------
# Run Flask Server
# -----------------------------------
if __name__ == '__main__':

    app.run(
        debug=True,
        host='0.0.0.0',
        port=5000
    )