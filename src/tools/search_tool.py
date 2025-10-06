from typing import Dict, Any
from langchain.tools import BaseTool
import json
from pathlib import Path
import sys
sys.path.append(str(Path(__file__).parent.parent))
from job_search import query_and_save_jobs


class JobSearchTool(BaseTool):
    name: str = "job_searcher"
    description: str = """
    Search for jobs using the Adzuna API.
    Input should be a JSON string with 'query' and optional 'location'.
    
    Examples:
    - {"query": "AI engineer", "location": "Berlin"}
    - {"query": "Machine Learning", "location": "London"}
    - {"query": "Data Scientist"}
    
    Returns job postings from Adzuna API with titles, companies, descriptions, and apply links.
    """
    
    def _run(self, input_str: str) -> Dict[str, Any]:
        """Search for jobs"""
        try:
            input_data = json.loads(input_str)
        except json.JSONDecodeError:
            return {"error": "Invalid JSON input"}
        
        query = input_data.get("query")
        if not query:
            return {"error": "Query is required"}
        
        location = input_data.get("location", "Berlin")
        
        try:
            result = query_and_save_jobs(query=query, job_location=location)
            
            jobs = result.get("data", [])
            
            return {
                "status": "success",
                "total_jobs": len(jobs),
                "query": query,
                "location": location,
                "jobs": jobs
            }
        except Exception as e:
            return {"error": f"Job search failed: {str(e)}"}
    
    async def _arun(self, input_str: str) -> Dict[str, Any]:
        """Async version"""
        return self._run(input_str)

