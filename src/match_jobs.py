import json
from sklearn.metrics.pairwise import cosine_similarity
from embedding_utils import embed_text_list, expand_skills_with_embeddings
from text_preprocessing import lemmatize_text


def match_profile_to_jobs(profile, job_postings, top_n=5):
    '''
    Match a user profile against job postings.
    Expand skills with embeddings, lemmatize text, and calculate cosine similarity.
    Return top N matches.
    '''

    # 1. Prepare job text and lemmatize it for expansion
    job_texts = [
        job.get('job_title', '') + ' ' + job.get('job_description', '')
        for job in job_postings
    ]
    lemmatized_job_texts = [lemmatize_text(text) for text in job_texts]

    # 2. Expand skills using lemmatized job content
    expanded_skills = expand_skills_with_embeddings(profile.get("skills", []), lemmatized_job_texts)

    # 3. Compose profile text and lemmatize
    profile_text = ' '.join(
        expanded_skills +
        profile.get('experience', []) +
        profile.get('education', []) +
        profile.get('certifications', []) +
        profile.get('projects', [])
    )
    profile_text = lemmatize_text(profile_text)

    # 4. Embed and compare
    profile_embeddings = embed_text_list([profile_text])
    job_embeddings = embed_text_list(job_texts)

    cosine_similarities = cosine_similarity(profile_embeddings, job_embeddings).flatten()

    # 5. Score and sort
    scored_jobs = list(zip(job_postings, cosine_similarities))
    scored_jobs.sort(key=lambda x: x[1], reverse=True)

    return [job for job, _ in scored_jobs[:top_n]]