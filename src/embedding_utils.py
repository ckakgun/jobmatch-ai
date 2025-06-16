from sentence_transformers import SentenceTransformer
from sentence_transformers import util

model = SentenceTransformer("all-MiniLM-L6-v2")

def expand_skills_with_embeddings(skills, possible_terms, top_k=2):
    ''' 
    Expand a list of skills with their embeddings.
    Returns a list of expanded skills.
    '''
    skill_embeddings = model.encode(skills, convert_to_tensor=True)
    all_term_embeddings = model.encode(possible_terms, convert_to_tensor=True)

    expanded = set(skills)
    for i, skill_emb in enumerate(skill_embeddings):
        similarities = util.pytorch_cos_sim(skill_emb, all_term_embeddings)[0]
        top_indices = similarities.topk(top_k).indices
        for idx in top_indices:
            expanded.add(possible_terms[idx])
    return list(expanded)


def embed_text_list(text_list):
    '''
    Embed a list of text strings using the SentenceTransformer model.
    Returns a numpy array of embeddings.
    '''

    if not text_list:
        return []
    
    return model.encode(text_list)




