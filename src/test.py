# test_adzuna.py
import requests
import os
from dotenv import load_dotenv

load_dotenv()

def test_adzuna_api():
    """Adzuna API'yi test et"""
    app_id = os.getenv("ADZUNA_APP_ID")
    app_key = os.getenv("ADZUNA_APP_KEY")
    
    if not app_id or not app_key:
        print("❌ Adzuna API credentials not found")
        return False
    
    url = "https://api.adzuna.com/v1/api/jobs/de/search/1"
    params = {
        "app_id": app_id,
        "app_key": app_key,
        "what": "AI engineer",
        "where": "Berlin",
        "results_per_page": 10,
        "content-type": "application/json"
    }
    
    try:
        response = requests.get(url, params=params)
        if response.status_code == 200:
            data = response.json()
            jobs = data.get("results", [])
            print(f"✅ Adzuna API working! Found {len(jobs)} jobs")
            
            if jobs:
                print("\n📋 Sample jobs:")
                for i, job in enumerate(jobs[:3], 1):
                    print(f"{i}. {job.get('title', 'N/A')}")
                    print(f"   Company: {job.get('company', {}).get('display_name', 'N/A')}")
                    print(f"   Location: {job.get('location', {}).get('display_name', 'N/A')}")
                    print()
            return True
        else:
            print(f"❌ API Error: {response.status_code}")
            print(f"Response: {response.text}")
            return False
    except Exception as e:
        print(f"❌ Request Error: {e}")
        return False

if __name__ == "__main__":
    test_adzuna_api()