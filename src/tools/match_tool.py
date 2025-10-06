from typing import Dict, Any
from langchain.tools import BaseTool
import json
from pathlib import Path
import sys
sys.path.append(str(Path(__file__).parent.parent))
from match_jobs import match_profile_to_jobs


class JobMatcherTool(BaseTool):
    name: str = "job_matcher"
    description: str = """
    Match a user profile to job postings using embeddings and similarity.
    Input should be a JSON string with 'profile' (dict) and 'jobs' (list).
    Optional 'top_n' parameter (default: 3).
    
    Examples:
    - {"profile": {...}, "jobs": [...], "top_n": 5}
    - {"profile": {...}, "jobs": [...]}
    
    Returns top N matched jobs ranked by similarity score.
    Profile should contain: skills, experience, education, certifications.
    """
    
    def _run(self, input_str: str) -> Dict[str, Any]:
        """Match profile to jobs"""
        try:
            input_data = json.loads(input_str)
        except json.JSONDecodeError:
            return {"error": "Invalid JSON input"}
        
        profile = input_data.get("profile")
        jobs = input_data.get("jobs")
        
        if not profile:
            return {"error": "Profile is required"}
        if not jobs:
            return {"error": "Jobs list is required"}
        
        top_n = input_data.get("top_n", 3)
        
        try:
            matches = match_profile_to_jobs(profile, jobs, top_n=top_n)
            
            return {
                "status": "success",
                "total_jobs": len(jobs),
                "top_matches": len(matches),
                "matches": matches
            }
        except Exception as e:
            return {"error": f"Job matching failed: {str(e)}"}
    
    async def _arun(self, input_str: str) -> Dict[str, Any]:
        """Async version"""
        return self._run(input_str)

