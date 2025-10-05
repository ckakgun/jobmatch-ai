import json

from langchain_community.document_loaders import PyMuPDFLoader

default_path = 'data/linkedin_profile.pdf'

def extract_text_from_pdf(path):
    '''
    Extract linkedin profile text from a pdf file
    '''
    loader = PyMuPDFLoader(path)
    docs = loader.load()
    text = docs[0].page_content  
    return text


def parse_profile(text):
    '''
    Parse the text to get the profile information
    '''

    profile = {
        "name": "Ceren Kaya Akgün",  
        "headline": "Freelance NLP & Data Science Projects",  
        "skills": ["Machine Learning Algorithms", "Pandas", "Natural Language Processing (NLP)"],  # known
        "languages": ["English", "German", "Turkish"],  
        "certifications": [],  
        "experience": [],  
        "education": []  
    }
    # parse the certifications
    lines = text.split('\n')
    certifications_index = None
    for i, line in enumerate(lines):
        if line.strip().lower() == 'certifications':
            certifications_index = i
            break
    certifications = []
    if certifications_index is not None:
        for i in range(certifications_index +1 , len(lines)):
            line_clean = lines[i].strip()
            if line_clean == '' or line_clean.lower() in ['experience', 'education']:
                break
            certifications.append(line_clean)   
    profile['certifications'] = certifications
    # parse the experience
    experience_index = None
    for j , line in enumerate(lines):
        if line.strip().lower() == 'experience':
            experience_index = j
            break
    experience = []
    if experience_index is not None:
        for i in range(experience_index +1 , len(lines)):
            line_clean = lines[i].strip()
            if line_clean == '' or line_clean.lower() in ['education']:
                break
            experience.append(line_clean)   
    profile['experience'] = experience
    # parse the education
    education_index = None
    for k, line in enumerate(lines):
        if line.strip().lower() == 'education':
            education_index = k
            break
    education = []
    if education_index is not None:
        for i in range(education_index +1, len(lines)):
            line_clean = lines[i].strip()
            if line_clean == '' or line_clean.lower() in ['skills']:
                break
            education.append(line_clean)   
    profile['education'] = education
    # parse the skills
    skills_index = None
    for l, line in enumerate(lines):
        if line.strip().lower() == 'skills':
            skills_index = l
            break
    skills = []
    if skills_index is not None:
        for i in range(skills_index +1, len(lines)):
            line_clean = lines[i].strip()
            if line_clean == '' or line_clean.lower() in ['languages']:
                break
            skills.append(line_clean)   
    profile['skills'] = skills
    return profile
