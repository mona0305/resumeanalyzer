import docx
import PyPDF2
import spacy
from nltk.tokenize import word_tokenize

nlp = spacy.load('en_core_web_sm')

def parse_resume(file_path):
    # Initialize variables
    name = "Unknown"
    skills = []
    location = "Unknown"
    
    # Read PDF or DOCX file
    if file_path.endswith('.pdf'):
        with open(file_path, 'rb') as file:
            reader = PyPDF2.PdfReader(file)
            text = ''
            for page in reader.pages:
                text += page.extract_text()
    elif file_path.endswith('.docx'):
        doc = docx.Document(file_path)
        text = '\n'.join([para.text for para in doc.paragraphs])
    else:
        text = ""

    # Tokenize and extract skills (dummy skills for now)
    skills = ['Python', 'JavaScript', 'HTML', 'CSS']  # Replace with actual extraction later

    # Use spaCy to parse text for name and location
    doc_nlp = nlp(text)
    for ent in doc_nlp.ents:
        if ent.label_ == 'PERSON' and name == "Unknown":
            name = ent.text
        elif ent.label_ == 'GPE' and location == "Unknown":
            location = ent.text
    
    return {
        "name": name,
        "skills": skills,
        "location": location
    }
