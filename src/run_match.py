from parse_profile import extract_text_from_pdf, parse_profile
from match_jobs import match_profile_to_jobs
from job_search import query_and_save_jobs
import json

path = "data/linkedin_profile.pdf"
profile_path = "data/linkedin_profile.json"
job_postings_path = "data/job_postings.json"

if __name__ == "__main__":
    # 1. Extract & parse profile
    text = extract_text_from_pdf(path)
    profile = parse_profile(text)
    
    with open(profile_path, "w", encoding="utf-8") as f:
        json.dump(profile, f, indent=4)

    # 2. Fetch jobs and load from file
    query_and_save_jobs(query="AI engineer")

    with open(job_postings_path, encoding="utf-8") as f:
        job_data = json.load(f)
    job_postings = job_data.get("data", [])
    
    print(f"📊 Total jobs fetched: {len(job_postings)}")
    
    # Debug: Show sample jobs
    if job_postings:
        print("\n🔍 Sample jobs:")
        for i, job in enumerate(job_postings[:3], 1):
            print(f"{i}. Title: {job.get('job_title', 'N/A')}")
            print(f"   Company: {job.get('employer_name', 'N/A')}")
            print(f"   Location: {job.get('job_city', 'N/A')}")
            print(f"   Country: {job.get('job_country', 'N/A')}")
            print()

    # 3. Relaxed filtering for debugging
    def filter_jobs(jobs):
        filtered = []
        print(f"\n🔍 Filtering {len(jobs)} jobs...")
        
        for job_idx, job_item in enumerate(jobs):
            # Location filtering (more flexible)
            country = (job_item.get('job_country') or '').lower()
            
            # Accept jobs from Germany, US, UK, Canada, Netherlands
            valid_countries = ['de', 'germany', 'us', 'usa', 'united states',
                             'gb', 'uk', 'united kingdom', 'ca', 'canada',
                             'nl', 'netherlands']
            
            # Job type filtering (more lenient)
            job_type = (job_item.get('job_employment_type') or '').lower()
            valid_types = ['full-time', 'fulltime', 'full time', 'contract', 'permanent', 'remote', 'part-time']
            
            # Title relevance filtering (more lenient)
            title = (job_item.get('job_title') or '').lower()
            description = (job_item.get('job_description') or '').lower()
            
            # Broader AI/tech keywords
            ai_keywords = [
                'ai', 'artificial intelligence', 'machine learning', 'ml', 'nlp', 'llm',
                'data scientist', 'data engineer', 'software engineer', 'developer',
                'engineer', 'analyst', 'researcher', 'scientist', 'specialist',
                'python', 'java', 'javascript', 'react', 'node', 'sql', 'database'
            ]
            
            # Check relevance
            title_match = any(keyword in title for keyword in ai_keywords)
            desc_match = any(keyword in description for keyword in ai_keywords)
            is_relevant = title_match or desc_match
            
            # Check filters
            country_match = any(country_code in country for country_code in valid_countries)
            type_match = not job_type or any(jt in job_type for jt in valid_types)
            
            # Apply relaxed filters
            if country_match and type_match and is_relevant:
                filtered.append(job_item)
                print(f"✅ Job {job_idx+1}: {job_item.get('job_title', 'N/A')[:60]}...")
            else:
                print(f"❌ Job {job_idx+1}: {job_item.get('job_title', 'N/A')[:60]}... (filtered out)")
        
        return filtered

    filtered_jobs = filter_jobs(job_postings)
    print(f"📍 {len(filtered_jobs)} jobs after enhanced filtering")

    if not filtered_jobs:
        print("No jobs found.")
        exit()

    job_postings = filtered_jobs

    # 4. Match
    top_matches = match_profile_to_jobs(profile, job_postings, top_n=3)

    # 5. Display detailed results
    print(f"\n🎯 TOP {len(top_matches)} JOB MATCHES:")
    print("=" * 80)
    
    for i, job in enumerate(top_matches, 1):
        print(f"\n🔹 MATCH #{i}")
        print("-" * 50)
        print(f"📋 Title: {job.get('job_title', 'N/A')}")
        print(f"🏢 Company: {job.get('employer_name', 'N/A')}")
        print(f"📍 Location: {job.get('job_city', 'N/A')}, {job.get('job_country', 'N/A')}")
        print(f"💼 Employment Type: {job.get('job_employment_type', 'N/A')}")
        
        # Extract job level from title
        title = job.get('job_title', '').lower()
        if any(level in title for level in ['senior', 'sr', 'lead', 'principal', 'staff']):
            level = "Senior Level"
        elif any(level in title for level in ['junior', 'jr', 'entry', 'graduate', 'trainee']):
            level = "Junior Level"
        elif any(level in title for level in ['mid', 'intermediate']):
            level = "Mid Level"
        else:
            level = "Level Not Specified"
        print(f"📊 Level: {level}")
        
        # Check for remote work indicators
        description = job.get('job_description', '').lower()
        title_lower = title
        remote_indicators = ['remote', 'hybrid', 'work from home', 'wfh', 'distributed']
        is_remote = any(indicator in description or indicator in title_lower for indicator in remote_indicators)
        work_type = "Remote/Hybrid Available" if is_remote else "On-site"
        print(f"🏠 Work Type: {work_type}")
        
        print(f"🔗 Apply Link: {job.get('job_apply_link', 'N/A')}")
        print(f"📝 Description Preview: {job.get('job_description', 'N/A')[:200]}...")
        print("-" * 50)