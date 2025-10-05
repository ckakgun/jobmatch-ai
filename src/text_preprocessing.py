import spacy

def lemmatize_text(text):
    '''
    Lemmatize text string using spaCy.
    Returns a string of lemmatized tokens.
    '''
    try:
        nlp = spacy.load("en_core_web_sm")
    except OSError:
        print("spaCy model not found. Please run: python -m spacy download en_core_web_sm")
        return text.lower()
    
    doc = nlp(text.lower())
    lemmatized_tokens = [token.lemma_ for token in doc if not token.is_stop and not token.is_punct]
    return ' '.join(lemmatized_tokens)