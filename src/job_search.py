import os
import requests
import json
from dotenv import load_dotenv

load_dotenv()

def query_and_save_jobs(query, job_location="Berlin, Germany", output_path="data/job_postings.json"):
    """
    Search for jobs using the JSearch API with location filtering,
    log progress, and save results to a JSON file.
    """
    print(f"🔁 Fetching jobs for: '{query}' in '{job_location}'")
    
    headers = {
        "X-RapidAPI-Key": os.getenv("JSEARCH_API_KEY"),
        "X-RapidAPI-Host": "jsearch.p.rapidapi.com"
    }

    params = {
        'query': query,
        'countryCode': 'de',
        'city': 'Berlin',
        'page': 1,
        'num_pages': 1,
        'employment_type': 'full_time',
        'sort': 'newest',
        'limit': 10,
    }

    url = 'https://jsearch.p.rapidapi.com/search'
    response = requests.get(url, headers=headers, params=params)

    if response.status_code == 200:
        data = response.json()
        num = len(data.get("data", []))
        print(f"✔️ Retrieved {num} job postings")
        
        with open(output_path, 'w') as f:
            json.dump(data, f, indent=4)
        print(f"💾 Saved to {output_path}")
        return data
    else:
        print(f"❗️ API Error: {response.status_code}")
        return {}