import os
import requests
import json
from dotenv import load_dotenv
load_dotenv()

def query_and_save_jobs(query, output_path="data/job_postings.json"):
    '''
    Search for jobs using the JSearch API and saves them to a json file
    '''
    headers = {
        "X-RapidAPI-Key": os.getenv("JSEARCH_API_KEY"), # get the api key from the .env file
        "X-RapidAPI-Host": "jsearch.p.rapidapi.com"
    }
    # Make GET request to JSearch API

    query = 'NLP Data Scientist Junior Machine Learning AI'
    url = 'https://jsearch.p.rapidapi.com/search'
    params = {
        'query': query,
        'location': 'Berlin, Germany', 
        'page': 1,
        'num_pages': 1,
        'date_posted': 'today',
        'employment_type': 'full_time',
        'sort': 'newest',
        'limit': 10,
    }
    # Save response['data'] to job_postings.json
    response = requests.get(url, headers = headers, params =params)
    if response.status_code == 200:
        data = response.json()
        with open(output_path, 'w') as f:
            json.dump(data, f, indent = 4)
    return data

if __name__ == "__main__":
    query = "NLP Data Scientist"
    data = query_and_save_jobs(query)
    print(data)