from parse_profile import extract_text_from_pdf, parse_profile
from match_jobs import match_profile_to_jobs
from job_search import query_and_save_jobs
import json

if __name__ == "__main__":
    # 1. Extract & parse profile
    text = extract_text_from_pdf("data/ceren_linkedin_profile.pdf")
    profile = parse_profile(text)
    
    with open("data/ceren_linkedin_profile.json", "w") as f:
        json.dump(profile, f, indent=4)

    # 2. Fetch jobs and load from file
    query_and_save_jobs(query="berlin nlp data scientist ")

    with open("data/job_postings.json") as f:
        job_data = json.load(f)
    job_postings = job_data.get("data", [])


    filtered_jobs = [
        job for job in job_postings
        if 'berlin' in (job.get('job_city') or '').lower()
        and job.get('job_country', '').lower() in ['de', 'germany']
    ]
    print(f"📍 {len(filtered_jobs)} jobs in Berlin, Germany after filtering")

    if not filtered_jobs:
        print("No jobs found in Berlin, Germany after filtering.")
        exit()

    job_postings = filtered_jobs

    # 3. Match
    top_matches = match_profile_to_jobs(profile, job_postings, top_n=3)

    # 4. Display
    for i, job in enumerate(top_matches, 1):
        print(f"\n🔹 Match #{i}")
        print(f"Title: {job['job_title']}")
        print(f"Company: {job.get('employer_name', 'N/A')}")
        print(f"Location: {job.get('job_city', 'N/A')}")
        print(f"Description: {job.get('job_description', 'N/A')[:300]}...")
        print(f"Apply Link: {job.get('job_apply_link', 'N/A')}")