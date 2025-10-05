import os
from langchain_huggingface import HuggingFaceEmbeddings
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
from dotenv import load_dotenv

load_dotenv()

# Use Hugging Face embeddings as fallback
model = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2",
    model_kwargs={'device': 'cpu'}
)


def expand_skills_with_embeddings(skills, possible_terms, top_k=2):
    ''' 
    Expand a list of skills with their embeddings.
    Returns a list of expanded skills.
    '''
    # Ensure inputs are lists of strings
    if not skills or not possible_terms:
        return skills if skills else []
    
    # Convert to strings if needed
    skills = [str(skill) for skill in skills if skill]
    possible_terms = [str(term) for term in possible_terms if term]
    
    if not skills or not possible_terms:
        return skills
    
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
    
    # Ensure all items are strings
    text_list = [str(text) for text in text_list if text]
    
    if not text_list:
        return []
    
    return np.array(model.embed_documents(text_list))




