import json
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity



def match_profile_to_jobs(profile, job_postings, top_n=5):
    '''
    Compare user profile against job postings.
    Score/rank them based on keyword/skill overlap.
    Return top N matches.
    '''
    profile_text = ' '.join(
        profile.get('skills', []) +
        profile.get('experience', []) +
        profile.get('education', []) +
        profile.get('certifications', []) +
        profile.get('projects', [])
        )


    job_texts = [
        job.get('job_title', '') + ' ' + job.get('job_description', '')
        for job in job_postings
    ]

    documents = [profile_text] + job_texts

    vectorizer =TfidfVectorizer(stop_words='english')
    documents_vector = vectorizer.fit_transform(documents)

    cosine_similarities = cosine_similarity(
        documents_vector[0:1], documents_vector[1:]
    ).flatten()


    scored_jobs = list(zip(job_postings, cosine_similarities))
    scored_jobs.sort(key = lambda x: x[1], reverse=True)


    top_matches = [job for job, score in scored_jobs[:top_n]]

    return top_matches
