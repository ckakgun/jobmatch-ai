from typing import Dict, Any, Optional
from langchain.tools import BaseTool
from pydantic import Field
import json
from pathlib import Path
import sys
sys.path.append(str(Path(__file__).parent.parent))
from parse_profile import extract_text_from_pdf, parse_profile


class ProfileParserTool(BaseTool):
    name: str = "profile_parser"
    description: str = """
    Parse a user profile from PDF or JSON.
    Input should be a JSON string with 'source' (pdf/json/dict) and 'path' or 'data'.
    
    Examples:
    - {"source": "pdf", "path": "data/resume.pdf"}
    - {"source": "json", "path": "data/profile.json"}
    - {"source": "dict", "data": {"name": "John", "skills": ["Python"]}}
    
    Returns a structured profile dictionary with skills, experience, education, etc.
    """
    
    def _run(self, input_str: str) -> Dict[str, Any]:
        """Parse profile from various sources"""
        try:
            input_data = json.loads(input_str)
        except json.JSONDecodeError:
            return {"error": "Invalid JSON input"}
        
        source = input_data.get("source", "").lower()
        
        if source == "pdf":
            path = input_data.get("path")
            if not path:
                return {"error": "PDF path required"}
            
            try:
                text = extract_text_from_pdf(path)
                profile = parse_profile(text)
                return {
                    "status": "success",
                    "profile": profile,
                    "source": "pdf"
                }
            except Exception as e:
                return {"error": f"PDF parsing failed: {str(e)}"}
        
        elif source == "json":
            path = input_data.get("path")
            if not path:
                return {"error": "JSON path required"}
            
            try:
                with open(path, 'r', encoding='utf-8') as f:
                    profile = json.load(f)
                return {
                    "status": "success",
                    "profile": profile,
                    "source": "json"
                }
            except Exception as e:
                return {"error": f"JSON loading failed: {str(e)}"}
        
        elif source == "dict":
            data = input_data.get("data")
            if not data:
                return {"error": "Profile data required"}
            
            return {
                "status": "success",
                "profile": data,
                "source": "dict"
            }
        
        else:
            return {"error": f"Unknown source: {source}. Use 'pdf', 'json', or 'dict'"}
    
    async def _arun(self, input_str: str) -> Dict[str, Any]:
        """Async version"""
        return self._run(input_str)

