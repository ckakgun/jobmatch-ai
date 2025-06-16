import json


def match_profile_to_jobs(profile, job_postings, top_n=3):
    '''
    Compare user profile against job postings.
    Score/rank them based on keyword/skill overlap.
    Return top N matches.
    '''

    scored_jobs = []

    for job in job_postings:
        title = job.get('job_title', '').lower()
        description = job.get('job_description', '').lower()
        job_text = f"{title} {description}"

        score = 0
        for skill in profile['skills']:
            if skill.lower() in job_text:
                score += 1

        scored_jobs.append((job, score))

    scored_jobs.sort(key=lambda x: x[1], reverse=True)
    top_matches = [job for job, score in scored_jobs[:top_n]]

    return top_matches
