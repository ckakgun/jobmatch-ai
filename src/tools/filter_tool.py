from typing import Dict, Any, List
from langchain.tools import BaseTool
import json


class JobFilterTool(BaseTool):
    name: str = "job_filter"
    description: str = """
    Filter jobs based on location, type, and relevance criteria.
    Input should be a JSON string with 'jobs' (list) and optional filters:
    - 'countries': list of valid country codes (default: ['de', 'uk', 'nl'])
    - 'job_types': list of valid job types (default: ['full-time', 'contract', 'remote'])
    - 'keywords': list of required keywords for relevance
    
    Examples:
    - {"jobs": [...], "countries": ["de", "uk"], "keywords": ["ai", "ml"]}
    - {"jobs": [...], "job_types": ["remote", "full-time"]}
    
    Returns filtered list of jobs matching the criteria.
    """
    
    def _run(self, input_str: str) -> Dict[str, Any]:
        """Filter jobs based on criteria"""
        try:
            input_data = json.loads(input_str)
        except json.JSONDecodeError:
            return {"error": "Invalid JSON input"}
        
        jobs = input_data.get("jobs", [])
        if not jobs:
            return {"error": "Jobs list is required"}
        
        valid_countries = input_data.get("countries", ['de', 'germany', 'uk', 'united kingdom', 'nl', 'netherlands'])
        valid_types = input_data.get("job_types", ['full-time', 'fulltime', 'contract', 'permanent', 'remote'])
        keywords = input_data.get("keywords", [
            'ai', 'artificial intelligence', 'machine learning', 'ml', 'nlp', 
            'data scientist', 'engineer', 'developer', 'python'
        ])
        
        filtered = []
        
        for job in jobs:
            country = (job.get('job_country') or '').lower()
            job_type = (job.get('job_employment_type') or '').lower()
            title = (job.get('job_title') or '').lower()
            description = (job.get('job_description') or '').lower()
            
            country_match = any(c in country for c in valid_countries)
            type_match = not job_type or any(jt in job_type for jt in valid_types)
            
            keyword_match = any(
                kw in title or kw in description 
                for kw in keywords
            )
            
            if country_match and type_match and keyword_match:
                filtered.append(job)
        
        return {
            "status": "success",
            "total_input": len(jobs),
            "total_filtered": len(filtered),
            "filter_rate": f"{len(filtered)/len(jobs)*100:.1f}%",
            "jobs": filtered
        }
    
    async def _arun(self, input_str: str) -> Dict[str, Any]:
        """Async version"""
        return self._run(input_str)

