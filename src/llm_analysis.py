import os
from typing import Dict, List, Optional

try:
    from openai import OpenAI
except ImportError:
    OpenAI = None

try:
    from groq import Groq
except ImportError:
    Groq = None

SYSTEM_PROMPT = "You are an expert career coach who writes concise, structured compatibility analyses. Highlight strengths, potential gaps, and actionable advice."


def _select_provider(preferred: Optional[str] = None) -> str:
    if preferred:
        return preferred
    env_value = os.getenv("JOBMATCH_LLM_PROVIDER")
    if env_value:
        return env_value
    if os.getenv("OPENAI_API_KEY"):
        return "openai"
    if os.getenv("GROQ_API_KEY"):
        return "groq"
    return ""


def _build_profile_block(profile: Dict) -> str:
    parts: List[str] = []
    name = profile.get("name")
    if name:
        parts.append(f"Name: {name}")
    headline = profile.get("headline")
    if headline:
        parts.append(f"Headline: {headline}")
    for field in ["skills", "experience", "education", "certifications", "projects", "languages"]:
        values = profile.get(field)
        if values:
            joined = " | ".join(values)
            parts.append(f"{field.title()}: {joined}")
    return "\n".join(parts)


def _build_job_block(job: Dict) -> str:
    parts: List[str] = []
    title = job.get("job_title")
    if title:
        parts.append(f"Title: {title}")
    company = job.get("employer_name")
    if company:
        parts.append(f"Company: {company}")
    location = job.get("job_city")
    if location:
        parts.append(f"Location: {location}")
    description = job.get("job_description")
    if description:
        parts.append(f"Description: {description}")
    return "\n".join(parts)


def _call_openai(prompt: str, model: Optional[str]) -> str:
    if OpenAI is None:
        raise RuntimeError("openai package not available")
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise RuntimeError("OPENAI_API_KEY missing")
    client = OpenAI(api_key=api_key)
    response = client.chat.completions.create(
        model=model or os.getenv("JOBMATCH_OPENAI_MODEL", "gpt-4o-mini"),
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": prompt},
        ],
        temperature=0.2,
    )
    return response.choices[0].message.content.strip()


def _call_groq(prompt: str, model: Optional[str]) -> str:
    if Groq is None:
        raise RuntimeError("groq package not available")
    api_key = os.getenv("GROQ_API_KEY")
    if not api_key:
        raise RuntimeError("GROQ_API_KEY missing")
    client = Groq(api_key=api_key)
    response = client.chat.completions.create(
        model=model or os.getenv("JOBMATCH_GROQ_MODEL", "llama3-70b-8192"),
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": prompt},
        ],
        temperature=0.2,
    )
    return response.choices[0].message.content.strip()


def analyze_match(profile: Dict, job: Dict, provider: Optional[str] = None, model: Optional[str] = None) -> Optional[str]:
    selected = _select_provider(provider)
    if not selected:
        return None
    profile_text = _build_profile_block(profile)
    job_text = _build_job_block(job)
    if not profile_text or not job_text:
        return None
    prompt = (
        "Candidate Profile:\n"
        + profile_text
        + "\n\nJob Posting:\n"
        + job_text
        + "\n\nProvide a short compatibility analysis with bullet points for strengths, gaps, and tailored recommendations."
    )
    if selected.lower() == "openai":
        return _call_openai(prompt, model)
    if selected.lower() == "groq":
        return _call_groq(prompt, model)
    return None


def analyze_matches(profile: Dict, jobs: List[Dict], provider: Optional[str] = None, model: Optional[str] = None) -> List[Optional[str]]:
    results: List[Optional[str]] = []
    for job in jobs:
        try:
            results.append(analyze_match(profile, job, provider, model))
        except Exception:
            results.append(None)
    return results
