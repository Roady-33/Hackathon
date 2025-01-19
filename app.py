import os
import fitz  # PyMuPDF
from flask import Flask, request, jsonify, render_template, redirect, url_for
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'C:\\Users\\ecgam\\Documents\\4. minor HU\\Hackathon\\Scientific_paper'
app.config['ALLOWED_EXTENSIONS'] = {'pdf'}

# Controleer of het geüploade bestand een PDF is
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

# Functie om tekst uit PDF te extraheren
def extract_text_from_pdf(pdf_path):
    doc = fitz.open(pdf_path)
    text = ""
    for page in doc:
        text += page.get_text()
    return text

# TRIPOD checklist criteria
checklist = {
    "Title": [
        "Does the title clearly state that the study is about developing and/or validating a multivariable prediction model?"
    ],
    "Abstract": [
        "Does the abstract provide a summary of objectives, study design, setting, participants, sample size, predictors, outcome, statistical analysis, results, and conclusions?"
    ],
    "Introduction": [
        "Does the background explain the medical context and rationale for developing or validating the model?",
        "Does the objective specify whether the study describes the development or validation of the model, or both?"
    ],
    "Methods": [
        "Is the source of data described, including location, recruitment period, and follow-up?",
        "Are eligibility criteria for participants specified?",
        "Are details of sample size calculation or justification provided?",
        "Is the outcome to be predicted clearly defined and measured?",
        "Are predictors clearly defined and measured?",
        "Are model development methods described, including how predictors were selected?",
        "Is the final prediction model specified, including details of any transformations or interactions of predictors?",
        "Are measures of model performance, like discrimination and calibration, reported?",
        "Is internal validation (e.g., cross-validation or bootstrap) reported?"
    ],
    "Results": [
        "Are the number of participants, flow of participants through the study, and reasons for non-participation reported?",
        "Are the baseline characteristics of participants described?",
        "Are model performance metrics reported, including measures of discrimination and calibration?",
        "Are details of how the final prediction model was developed, including statistical methods, reported?",
        "Are results of any additional analyses (e.g., subgroups, sensitivity analyses) reported?"
    ],
    "Discussion": [
        "Are the limitations of the study, including any potential sources of bias, discussed?",
        "Are the implications of the findings for clinical practice, policy, and future research discussed?",
        "Does the conclusion provide a summary of the key findings, along with their relevance and implications?"
    ],
    "Other Information": [
        "Are the sources of funding and any role of the funders in the research reported?",
        "Are any potential conflicts of interest disclosed?"
    ]
}

# Functie om tekst te highlighten gebaseerd op checklist
def highlight_text(text, checklist):
    highlighted_text = text
    for section, criteria in checklist.items():
        for term in criteria:
            highlighted_text = highlighted_text.replace(term, f"**{term}**")
    return highlighted_text

# Functie om score te berekenen gebaseerd op checklist
def calculate_score(text, checklist):
    score = 0
    total_criteria = sum(len(criteria) for criteria in checklist.values())
    for criteria in checklist.values():
        for term in criteria:
            if term in text:
                score += 1
    return score / total_criteria

# Route voor de homepage
@app.route('/')
def index():
    return render_template('index.html')

# Route om een PDF-bestand te uploaden en analyseren
@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({"error": "No file part"}), 400
    file = request.files['file']
    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400
    if file and allowed_file(file.filename):
        try:
            filename = secure_filename(file.filename)
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(file_path)
            
            text = extract_text_from_pdf(file_path)
            highlighted_text = highlight_text(text, checklist)
            score = calculate_score(text, checklist)
            
            return redirect(url_for('pdf_viewer', filename=filename))
        except Exception as e:
            return jsonify({"error": str(e)}), 500
    return jsonify({"error": "File not allowed"}), 400

@app.route('/viewer')
def pdf_viewer():
    filename = request.args.get('filename')
    file_url = url_for('static', filename='uploads/' + filename)
    return redirect(f'/static/pdfjs/web/viewer.html?file={file_url}')

if __name__ == '__main__':
    if not os.path.exists(app.config['UPLOAD_FOLDER']):
        os.makedirs(app.config['UPLOAD_FOLDER'])
    app.run(debug=True, host='0.0.0.0', port=5000)
