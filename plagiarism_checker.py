from flask import Flask, request, render_template
from werkzeug.utils import secure_filename
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import PyPDF2
import docx
import os

app = Flask(__name__, template_folder="templates")

# Allowed file extensions
ALLOWED_EXTENSIONS = {'pdf', 'docx'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def extract_text_from_pdf(file):
    try:
        reader = PyPDF2.PdfReader(file)
        text = " ".join([page.extract_text() for page in reader.pages if page.extract_text()])
        return text
    except Exception as e:
        return f"Error reading PDF: {str(e)}"

def extract_text_from_docx(file):
    try:
        doc = docx.Document(file)
        text = " ".join([para.text for para in doc.paragraphs])
        return text
    except Exception as e:
        return f"Error reading DOCX: {str(e)}"

def get_text_from_file(file):
    if file.filename.endswith(".pdf"):
        return extract_text_from_pdf(file)
    elif file.filename.endswith(".docx"):
        return extract_text_from_docx(file)
    return None

def check_plagiarism(text1, text2):
    vectorizer = TfidfVectorizer().fit_transform([text1, text2])
    similarity = cosine_similarity(vectorizer)[0][1]
    return round(similarity * 100, 2)  # Convert to percentage

@app.route("/", methods=["GET", "POST"])
def home():
    similarity = None
    error_message = None

    if request.method == "POST":
        if 'file1' not in request.files or 'file2' not in request.files:
            error_message = "Both files are required."
        else:
            file1 = request.files['file1']
            file2 = request.files['file2']

            if file1.filename == "" or file2.filename == "":
                error_message = "Please select both files."
            elif not (allowed_file(file1.filename) and allowed_file(file2.filename)):
                error_message = "Only PDF or DOCX files are allowed."
            else:
                text1 = get_text_from_file(file1)
                text2 = get_text_from_file(file2)

                if text1.startswith("Error") or text2.startswith("Error"):
                    error_message = text1 if text1.startswith("Error") else text2
                else:
                    similarity = check_plagiarism(text1, text2)

    return render_template("index.html", similarity=str(similarity) if similarity is not None else None, error=error_message)

if __name__ == "__main__":
    app.config['TEMPLATES_AUTO_RELOAD'] = True
    app.run(debug=True)
