from typing import Dict, Any, List, Optional
import json
from pathlib import Path
import sys
sys.path.append(str(Path(__file__).parent.parent))
from tools import ProfileParserTool, JobSearchTool, JobFilterTool, JobMatcherTool


class JobMatchAgent:
    """
    Main agent orchestrator for job matching workflow.
    Coordinates tools to parse profiles, search jobs, filter, and match.
    """
    
    def __init__(self):
        self.profile_tool = ProfileParserTool()
        self.search_tool = JobSearchTool()
        self.filter_tool = JobFilterTool()
        self.match_tool = JobMatcherTool()
        
        self.tools = {
            'profile_parser': self.profile_tool,
            'job_searcher': self.search_tool,
            'job_filter': self.filter_tool,
            'job_matcher': self.match_tool
        }
    
    def run_workflow(
        self, 
        profile_source: str,
        profile_path: Optional[str] = None,
        profile_data: Optional[Dict] = None,
        job_query: str = "AI engineer",
        job_location: str = "Berlin",
        filter_countries: Optional[List[str]] = None,
        filter_keywords: Optional[List[str]] = None,
        top_n: int = 3
    ) -> Dict[str, Any]:
        """
        Run complete job matching workflow.
        
        Args:
            profile_source: 'pdf', 'json', or 'dict'
            profile_path: Path to PDF or JSON file
            profile_data: Direct profile dictionary
            job_query: Job search query
            job_location: Job location
            filter_countries: List of country codes
            filter_keywords: List of keywords for filtering
            top_n: Number of top matches to return
        
        Returns:
            Dictionary with workflow results
        """
        workflow_results = {
            "steps": [],
            "profile": None,
            "jobs_found": 0,
            "jobs_filtered": 0,
            "top_matches": []
        }
        
        # Step 1: Parse Profile
        print("🔄 Step 1: Parsing profile...")
        profile_input = {
            "source": profile_source
        }
        if profile_path:
            profile_input["path"] = profile_path
        if profile_data:
            profile_input["data"] = profile_data
        
        profile_result = self.profile_tool._run(json.dumps(profile_input))
        
        if "error" in profile_result:
            return {"error": f"Profile parsing failed: {profile_result['error']}"}
        
        profile = profile_result["profile"]
        workflow_results["profile"] = profile
        workflow_results["steps"].append({
            "step": 1,
            "name": "profile_parsing",
            "status": "success"
        })
        print(f"✅ Profile loaded: {profile.get('name', 'Unknown')}")
        
        # Step 2: Search Jobs
        print(f"\n🔄 Step 2: Searching jobs for '{job_query}' in {job_location}...")
        search_input = {
            "query": job_query,
            "location": job_location
        }
        
        search_result = self.search_tool._run(json.dumps(search_input))
        
        if "error" in search_result:
            return {"error": f"Job search failed: {search_result['error']}"}
        
        jobs = search_result["jobs"]
        workflow_results["jobs_found"] = len(jobs)
        workflow_results["steps"].append({
            "step": 2,
            "name": "job_search",
            "status": "success",
            "total_jobs": len(jobs)
        })
        print(f"✅ Found {len(jobs)} jobs")
        
        # Step 3: Filter Jobs
        print("\n🔄 Step 3: Filtering jobs...")
        filter_input = {
            "jobs": jobs
        }
        if filter_countries:
            filter_input["countries"] = filter_countries
        if filter_keywords:
            filter_input["keywords"] = filter_keywords
        
        filter_result = self.filter_tool._run(json.dumps(filter_input))
        
        if "error" in filter_result:
            return {"error": f"Job filtering failed: {filter_result['error']}"}
        
        filtered_jobs = filter_result["jobs"]
        workflow_results["jobs_filtered"] = len(filtered_jobs)
        workflow_results["steps"].append({
            "step": 3,
            "name": "job_filtering",
            "status": "success",
            "filtered_jobs": len(filtered_jobs),
            "filter_rate": filter_result["filter_rate"]
        })
        print(f"✅ Filtered to {len(filtered_jobs)} jobs ({filter_result['filter_rate']})")
        
        # Step 4: Match Jobs
        print("\n🔄 Step 4: Matching jobs to profile...")
        match_input = {
            "profile": profile,
            "jobs": filtered_jobs,
            "top_n": top_n
        }
        
        match_result = self.match_tool._run(json.dumps(match_input))
        
        if "error" in match_result:
            return {"error": f"Job matching failed: {match_result['error']}"}
        
        matches = match_result["matches"]
        workflow_results["top_matches"] = matches
        workflow_results["steps"].append({
            "step": 4,
            "name": "job_matching",
            "status": "success",
            "top_matches": len(matches)
        })
        print(f"✅ Found {len(matches)} top matches")
        
        return workflow_results
    
    def call_tool(self, tool_name: str, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Call a specific tool directly.
        
        Args:
            tool_name: Name of the tool to call
            input_data: Input data as dictionary
        
        Returns:
            Tool result
        """
        if tool_name not in self.tools:
            return {"error": f"Unknown tool: {tool_name}"}
        
        tool = self.tools[tool_name]
        input_str = json.dumps(input_data)
        
        return tool._run(input_str)
    
    def list_tools(self) -> List[Dict[str, str]]:
        """List all available tools"""
        return [
            {
                "name": name,
                "description": tool.description
            }
            for name, tool in self.tools.items()
        ]
    
    def display_results(self, workflow_results: Dict[str, Any]) -> None:
        """Display workflow results in a formatted way"""
        if "error" in workflow_results:
            print(f"\n❌ Error: {workflow_results['error']}")
            return
        
        print("\n" + "=" * 80)
        print("🎯 JOB MATCHING RESULTS")
        print("=" * 80)
        
        print(f"\n📊 Workflow Summary:")
        print(f"  • Profile: {workflow_results['profile'].get('name', 'Unknown')}")
        print(f"  • Jobs Found: {workflow_results['jobs_found']}")
        print(f"  • Jobs Filtered: {workflow_results['jobs_filtered']}")
        print(f"  • Top Matches: {len(workflow_results['top_matches'])}")
        
        print(f"\n🔹 Top {len(workflow_results['top_matches'])} Matches:")
        print("-" * 80)
        
        for i, job in enumerate(workflow_results['top_matches'], 1):
            print(f"\n#{i}. {job.get('job_title', 'N/A')}")
            print(f"    🏢 {job.get('employer_name', 'N/A')}")
            print(f"    📍 {job.get('job_city', 'N/A')}, {job.get('job_country', 'N/A')}")
            print(f"    🔗 {job.get('job_apply_link', 'N/A')}")
        
        print("\n" + "=" * 80)

