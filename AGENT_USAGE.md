# 🤖 JobMatch AI - Agent Architecture

## Overview

JobMatch AI now uses a modular **agent-based architecture** with tool calling capabilities. This makes the system more flexible, testable, and extensible.

## Architecture

```
┌─────────────────────────────────────────────────────────┐
│                  JobMatchAgent                          │
│              (Workflow Orchestrator)                    │
└─────────────────────────────────────────────────────────┘
                            │
        ┌───────────────────┼───────────────────┐
        │                   │                   │
        ▼                   ▼                   ▼
┌──────────────┐   ┌──────────────┐   ┌──────────────┐
│ProfileParser │   │ JobSearcher  │   │ JobFilter    │
│     Tool     │   │     Tool     │   │     Tool     │
└──────────────┘   └──────────────┘   └──────────────┘
                            │
                            ▼
                   ┌──────────────┐
                   │ JobMatcher   │
                   │     Tool     │
                   └──────────────┘
```

## Tools

### 1. ProfileParserTool
**Purpose:** Parse user profiles from various sources

**Input:**
```json
{
  "source": "pdf|json|dict",
  "path": "path/to/file",
  "data": {...}
}
```

**Output:**
```json
{
  "status": "success",
  "profile": {
    "name": "...",
    "skills": [...],
    "experience": [...],
    "education": [...],
    "certifications": [...]
  }
}
```

### 2. JobSearchTool
**Purpose:** Search for jobs using Adzuna API

**Input:**
```json
{
  "query": "AI engineer",
  "location": "Berlin"
}
```

**Output:**
```json
{
  "status": "success",
  "total_jobs": 50,
  "jobs": [...]
}
```

### 3. JobFilterTool
**Purpose:** Filter jobs based on criteria

**Input:**
```json
{
  "jobs": [...],
  "countries": ["de", "uk", "nl"],
  "job_types": ["full-time", "remote"],
  "keywords": ["ai", "ml", "python"]
}
```

**Output:**
```json
{
  "status": "success",
  "total_filtered": 35,
  "filter_rate": "70.0%",
  "jobs": [...]
}
```

### 4. JobMatcherTool
**Purpose:** Match profile to jobs using embeddings

**Input:**
```json
{
  "profile": {...},
  "jobs": [...],
  "top_n": 3
}
```

**Output:**
```json
{
  "status": "success",
  "top_matches": 3,
  "matches": [...]
}
```

## Usage

### 1. CLI (Command Line)

Basic usage:
```bash
python src/run_agent.py --pdf data/linkedin_profile.pdf
```

With custom parameters:
```bash
python src/run_agent.py \
  --pdf data/resume.pdf \
  --query "Machine Learning Engineer" \
  --location "London" \
  --top 5 \
  --countries de uk nl us
```

With keywords filtering:
```bash
python src/run_agent.py \
  --json data/profile.json \
  --query "AI engineer" \
  --keywords pytorch tensorflow nlp llm
```

### 2. Python API

```python
from agents import JobMatchAgent

# Initialize agent
agent = JobMatchAgent()

# Run full workflow
results = agent.run_workflow(
    profile_source="pdf",
    profile_path="data/linkedin_profile.pdf",
    job_query="AI engineer",
    job_location="Berlin",
    filter_countries=["de", "uk", "nl"],
    filter_keywords=["ai", "ml", "nlp"],
    top_n=3
)

# Display results
agent.display_results(results)
```

### 3. Direct Tool Calling

```python
from agents import JobMatchAgent

agent = JobMatchAgent()

# Call specific tool
result = agent.call_tool('job_searcher', {
    "query": "AI engineer",
    "location": "Berlin"
})

print(result)
```

### 4. List Available Tools

```python
from agents import JobMatchAgent

agent = JobMatchAgent()
tools = agent.list_tools()

for tool in tools:
    print(f"{tool['name']}: {tool['description']}")
```

## Workflow Execution

The agent follows a 4-step workflow:

1. **Profile Parsing** → Load and parse user profile
2. **Job Search** → Fetch jobs from Adzuna API  
3. **Job Filtering** → Filter by location, type, keywords
4. **Job Matching** → Match profile to jobs using embeddings

Each step is independent and can be called separately via `call_tool()`.

## Error Handling

All tools return consistent error format:
```json
{
  "error": "Error message description"
}
```

The agent workflow stops on error and returns the error message.

## Extending the System

### Add a New Tool

1. Create tool in `src/tools/`:
```python
from langchain.tools import BaseTool
import json

class MyCustomTool(BaseTool):
    name: str = "my_tool"
    description: str = "Tool description"
    
    def _run(self, input_str: str) -> dict:
        input_data = json.loads(input_str)
        # Tool logic here
        return {"status": "success", "result": "..."}
    
    async def _arun(self, input_str: str) -> dict:
        return self._run(input_str)
```

2. Register in `JobMatchAgent`:
```python
self.my_tool = MyCustomTool()
self.tools['my_tool'] = self.my_tool
```

3. Use in workflow or directly:
```python
result = agent.call_tool('my_tool', {"param": "value"})
```

## Benefits of Agent Architecture

✅ **Modularity** - Each tool is independent and reusable  
✅ **Testability** - Easy to test individual tools  
✅ **Extensibility** - Add new tools without changing core  
✅ **Flexibility** - Call tools in any order or combination  
✅ **Debugging** - Easy to debug individual steps  
✅ **Reusability** - Tools can be used in different workflows  

## Next Steps

- [ ] Add caching for job search results
- [ ] Implement async workflow execution
- [ ] Add LLM-based agent for dynamic tool selection
- [ ] Create web UI (Streamlit)
- [ ] Add API endpoints (FastAPI)
- [ ] Implement result ranking improvements

