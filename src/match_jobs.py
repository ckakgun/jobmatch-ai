import json

with open("data/job_postings.json") as f:
    job_data = json.load(f)
job_postings = job_data["data"]

with open("data/ceren_linkedin_profile.json") as f:
    profile = json.load(f)


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

if __name__ == "__main__":
    top_matches = match_profile_to_jobs(profile, job_postings)

    for i, job in enumerate(top_matches, 1):
        print(f"\n🔹 Match #{i}")
        print(f"Title: {job['job_title']}")
        print(f"Company: {job.get('employer_name', 'N/A')}")
        print(f"Location: {job.get('job_city', 'N/A')}")
        print(f"Description: {job['job_description'][:300]}...")