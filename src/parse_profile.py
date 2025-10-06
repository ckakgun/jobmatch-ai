import re

from langchain_community.document_loaders import PyMuPDFLoader

default_path = 'data/profile.pdf'

def extract_text_from_pdf(path):
    '''
    Extract linkedin profile text from a pdf file
    '''
    loader = PyMuPDFLoader(path)
    docs = loader.load()
    text = docs[0].page_content  
    return text


def normalize_heading(value):
    return re.sub(r'[^a-z ]+', '', value.lower()).strip()


def clean_entry(value):
    cleaned = value.replace('\u00a0', ' ').strip()
    cleaned = cleaned.lstrip(' *-\u2022\u00b7')
    cleaned = ' '.join(cleaned.split())
    return cleaned


def should_skip_line(value):
    lower = value.lower()
    if not value:
        return True
    if lower.startswith('page ') and ' of ' in lower:
        return True
    return False


def is_name_candidate(value):
    if any(char.isdigit() for char in value):
        return False
    tokens = [token for token in re.split(r'[\s\-]+', value) if token]
    if len(tokens) < 2 or len(tokens) > 5:
        return False
    valid = 0
    for token in tokens:
        if not token[0].isalpha():
            return False
        if token[0].isupper() or token.isupper():
            valid += 1
    return valid >= len(tokens) - 1


def is_headline_candidate(value):
    lower = value.lower()
    job_keywords = ['engineer', 'developer', 'scientist', 'manager', 'consultant', 'analyst', 'specialist', 'designer', 'researcher', 'lead', 'student', 'founder']
    dash_markers = [chr(8212), chr(8211), '|']
    if any(marker in value for marker in dash_markers) or ' - ' in value or ' -' in value or '- ' in value or ' at ' in lower or ' @ ' in lower:
        return True
    return any(keyword in lower for keyword in job_keywords)


def unique_preserve(items):
    seen = set()
    result = []
    for item in items:
        key = item.lower()
        if key in seen:
            continue
        seen.add(key)
        result.append(item)
    return result


def extract_name_headline(lines, headings):
    summary_positions = [idx for idx, label in headings if label == 'summary']
    limit = summary_positions[0] if summary_positions else len(lines)
    headline = ''
    name = ''
    index = limit - 1
    while index >= 0 and not lines[index].strip():
        index -= 1
    pointer = index
    while pointer >= 0:
        value = lines[pointer].strip()
        if not value:
            pointer -= 1
            continue
        if is_headline_candidate(value):
            headline = value
            pointer -= 1
            break
        pointer -= 1
    while pointer >= 0:
        value = lines[pointer].strip()
        if not value:
            pointer -= 1
            continue
        if is_name_candidate(value):
            name = value
            break
        pointer -= 1
    if not name or not headline:
        for i in range(len(lines) - 1):
            current = lines[i].strip()
            nxt = lines[i + 1].strip()
            if not name and is_name_candidate(current) and is_headline_candidate(nxt):
                name = current
                if not headline:
                    headline = nxt
                break
    return name, headline


def parse_profile(text):
    lines = text.splitlines()
    alias_map = {
        'summary': 'summary',
        'experience': 'experience',
        'education': 'education',
        'skills': 'skills',
        'top skills': 'skills',
        'languages': 'languages',
        'certifications': 'certifications',
        'contact': 'contact',
        'honors awards': 'ignore',
        'honorsawards': 'ignore',
        'publications': 'ignore'
    }
    headings = []
    for idx, raw in enumerate(lines):
        canonical = alias_map.get(normalize_heading(raw))
        if canonical:
            headings.append((idx, canonical))
    sections = {
        'summary': [],
        'skills': [],
        'languages': [],
        'certifications': [],
        'experience': [],
        'education': []
    }
    for position, label in headings:
        next_index = next((idx for idx, _ in headings if idx > position), len(lines))
        if label not in sections:
            continue
        entries = []
        for line_index in range(position + 1, next_index):
            entry = clean_entry(lines[line_index])
            if should_skip_line(entry):
                continue
            if entry:
                entries.append(entry)
        if entries:
            sections[label].extend(entries)
    name, headline = extract_name_headline(lines, headings)
    profile = {
        'name': name,
        'headline': headline,
        'skills': unique_preserve(sections['skills']),
        'languages': unique_preserve(sections['languages']),
        'certifications': unique_preserve(sections['certifications']),
        'experience': sections['experience'],
        'education': sections['education']
    }
    return profile
