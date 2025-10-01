from langchain_text_splitters import RecursiveCharacterTextSplitter

def lemmatize_text(text):
    '''
    Lemmatize text string using langchain_text_splitters.
    Returns a string of lemmatized tokens.
    '''
    text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=1000,
    chunk_overlap=200)
    text = text.lower()
    chunks = text_splitter.split_text(text)
    return chunks