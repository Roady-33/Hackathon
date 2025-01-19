import os
import fitz  # PyMuPDF

def extract_text_from_pdfs_in_folder(folder_path):
    all_text = {}
    for filename in os.listdir(folder_path):
        if filename.endswith(".pdf"):
            pdf_path = os.path.join(folder_path, filename)
            doc = fitz.open(pdf_path)
            text = ""
            for page in doc:
                text += page.get_text()
            all_text[filename] = text
    return all_text

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

# Voorbeeldgebruik
folder_path = r"C:\Users\ecgam\Documents\4. minor HU\Hackathon\Scientific_paper"  # Vervang dit door het pad naar je eigen map met PDF-bestanden
pdf_texts = extract_text_from_pdfs_in_folder(folder_path)
for filename, text in pdf_texts.items():
    highlighted_text = highlight_text(text, checklist)
    score = calculate_score(text, checklist)
    print(f"Highlighted Text from {filename}:")
    print(highlighted_text)
    print(f"Score: {score}")
    print("\n\n")
