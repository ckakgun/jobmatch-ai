import os
import requests
import json
from dotenv import load_dotenv

load_dotenv()

def query_and_save_jobs(query, job_location="Berlin, Germany", output_path="data/job_postings.json"):
    """
    Search for jobs using the Adzuna API with location filtering,
    log progress, and save results to a JSON file.
    """
    print(f"🔁 Fetching jobs for: '{query}' in '{job_location}'")
    
    # Adzuna API credentials
    app_id = os.getenv("ADZUNA_APP_ID")
    app_key = os.getenv("ADZUNA_APP_KEY")
    
    if not app_id or not app_key:
        print("❌ Adzuna API credentials not found. Please add ADZUNA_APP_ID and ADZUNA_APP_KEY to your .env file")
        print("📝 Get free API keys at: https://developer.adzuna.com/")
        return {}
    
    # Adzuna API parameters
    params = {
        'app_id': app_id,
        'app_key': app_key,
        'what': query,
        'where': 'Berlin',
        'results_per_page': 50,
        'content-type': 'application/json'
    }

    url = 'https://api.adzuna.com/v1/api/jobs/de/search/1'
    response = requests.get(url, params=params)

    if response.status_code == 200:
        data = response.json()
        num = len(data.get("results", []))
        print(f"✔️ Retrieved {num} job postings from Adzuna")
        
        # Debug: Print raw data structure
        if data.get("results"):
            print("🔍 Sample raw job data:")
            sample_job = data["results"][0]
            print(f"Keys: {list(sample_job.keys())}")
            print(f"Title: {sample_job.get('title', 'N/A')}")
            print(f"Company: {sample_job.get('company', {})}")
            print(f"Location: {sample_job.get('location', {})}")
        
        # Transform Adzuna format to match existing structure
        transformed_data = {
            "status": "OK",
            "data": []
        }
        
        for job in data.get("results", []):
            # Extract location info more carefully
            location_info = job.get("location", {})
            city = "Berlin"  # Default
            if isinstance(location_info, dict):
                if "area" in location_info and location_info["area"]:
                    city = location_info["area"][0] if isinstance(location_info["area"], list) else location_info["area"]
                elif "display_name" in location_info:
                    city = location_info["display_name"]
            
            transformed_job = {
                "job_id": str(job.get("id", "")),
                "job_title": job.get("title", ""),
                "employer_name": job.get("company", {}).get("display_name", ""),
                "job_description": job.get("description", ""),
                "job_city": city,
                "job_country": "DE",
                "job_apply_link": job.get("redirect_url", ""),
                "job_employment_type": "Full-time",
                "job_publisher": "Adzuna"
            }
            transformed_data["data"].append(transformed_job)
        
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(transformed_data, f, indent=4)
        print(f"💾 Saved {len(transformed_data['data'])} jobs to {output_path}")
        return transformed_data
    else:
        print(f"❗️ Adzuna API Error: {response.status_code}")
        print(f"Response: {response.text}")
        return {}