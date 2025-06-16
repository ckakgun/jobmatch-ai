import spacy
nlp = spacy.load("en_core_web_sm")

def lemmatize_text(text):
    '''
    Lemmatize a text string using spaCy.
    Returns a string of lemmatized tokens.
    '''
    doc = nlp(text.lower())
    return ' '.join([token.lemma_ for token in doc if not token.is_punct and not token.is_stop])