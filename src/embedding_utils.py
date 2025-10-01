import os
from langchain_openai import OpenAIEmbeddings
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv("OPENAI_API_KEY")
if not api_key:
    raise ValueError("OPENAI_API_KEY environment variable is not set. Please add it to your .env file.")

model = OpenAIEmbeddings(
    model="text-embedding-3-large",
    openai_api_key=api_key
)


def expand_skills_with_embeddings(skills, possible_terms, top_k=2):
    ''' 
    Expand a list of skills with their embeddings.
    Returns a list of expanded skills.
    '''
    skill_embeddings = model.embed_documents(skills)
    all_term_embeddings = model.embed_documents(possible_terms)

    expanded = set(skills)
    for skill_emb in skill_embeddings:
        similarities = cosine_similarity([skill_emb], all_term_embeddings)[0]
        top_indices = np.argsort(similarities)[-top_k:]
        for idx in top_indices:
            expanded.add(possible_terms[idx])
    return list(expanded)


def embed_text_list(text_list):
    '''
    Embed a list of text strings using OpenAI embeddings.
    Returns a numpy array of embeddings.
    '''
    if not text_list:
        return []
    
    return np.array(model.embed_documents(text_list))




