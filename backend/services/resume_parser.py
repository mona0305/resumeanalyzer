
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
        text = '
'.join([para.text for para in doc.paragraphs])
    
    # Tokenize and extract skills (dummy skills for now)
    skills = ['Python', 'JavaScript', 'HTML', 'CSS']  # Example skills
    
    # Use spaCy or any NLP method to parse text for name and location
    doc = nlp(text)
    for ent in doc.ents:
        if ent.label_ == 'PERSON':
            name = ent.text
        elif ent.label_ == 'GPE':  # Geopolitical entity, could be location
            location = ent.text
    
    return {
        "name": name,
        "skills": skills,
        "location": location
    }
    