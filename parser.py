# parser.py
import spacy
import re
import pandas as pd

# Load the spaCy model once
try:
    nlp = spacy.load("en_core_web_sm")
except OSError:
    print("Error: spaCy model 'en_core_web_sm' not found. Please run 'python -m spacy download en_core_web_sm'")
    nlp = None

# A sample list of skills for demonstration (expand this for better results)
SKILLS_LIST = [
    'Python', 'Streamlit', 'SpaCy', 'Pandas', 'SQL', 'Machine Learning', 
    'NLP', 'Data Analysis', 'Flask', 'Django', 'API', 'Git', 'Agile'
]

def clean_text(text):
    """Cleans and preprocesses the text[cite: 2]."""
    text = text.replace('\n', ' ')
    # Basic cleaning to keep only necessary characters
    text = re.sub(r'[^a-zA-Z0-9\s\.\,\@\-\/\(\)]', ' ', text)
    # Remove extra spaces
    text = re.sub(' +', ' ', text).strip()
    return text

def extract_contact_info(text):
    """Basic extraction of email and phone numbers using regex."""
    email = re.findall(r"[a-z0-9\.\-+_]+@[a-z0-9\.\-+_]+\.[a-z]+", text, re.I)
    phone_pattern = r'(\d{3}[-\.\s]??\d{3}[-\.\s]??\d{4}|\(\d{3}\)\s*\d{3}[-\.\s]??\d{4}|\d{10})'
    phone = re.findall(phone_pattern, text)
    
    # Flatten the list of phone matches and return unique results
    flat_phone = [p[0] if isinstance(p, tuple) and p else p for p in phone]
    return {'email': list(set(email)), 'phone': list(set([p.replace(' ', '').replace('-', '') for p in flat_phone if len(p) >= 10]))}

def extract_skills(text):
    """Identifies skills by matching against the predefined list."""
    found_skills = set()
    cleaned_text = text.lower()
    for skill in SKILLS_LIST:
        # Use regex for whole word match to avoid false positives
        if re.search(r'\b' + re.escape(skill.lower()) + r'\b', cleaned_text):
            found_skills.add(skill)
    return list(found_skills)

def extract_name(text):
    """Attempts to extract a name using spaCy's NER (PERSON)."""
    if not nlp: return "N/A (NLP Model Failed)"
    doc = nlp(text)
    for ent in doc.ents:
        if ent.label_ == 'PERSON':
            # Simple heuristic: assume the first person entity is the candidate's name
            return ent.text.split('\n')[0].strip()
    return "N/A"

def parse_resume(raw_text):
    """The main function to parse the resume text[cite: 3, 4]."""
    text = clean_text(raw_text)

    name = extract_name(text)
    contact_info = extract_contact_info(text)
    skills = extract_skills(text)

    # Organize output into JSON or table format [cite: 4]
    parsed_data = {
        'Name': name,
        'Email': contact_info['email'][0] if contact_info['email'] else 'N/A',
        'Phone': contact_info['phone'][0] if contact_info['phone'] else 'N/A',
        'Skills Found': ', '.join(skills) if skills else 'N/A',
        'Raw Text Snippet': text[:500] + '...' 
    }

    return parsed_data