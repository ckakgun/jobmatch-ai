# jobmatch-ai

## Project Name and Purpose
JobMatch AI – An intelligent tool to find jobs that match your LinkedIn profile using NLP.

## One-Sentence Summary
Find jobs that match your LinkedIn profile using NLP.

## Technologies Used
- Python
- Sentence Transformers
- Cosine Similarity
- PDF Parsing (PyMuPDF)
- JSearch API

## How It Works
1. **PDF Upload:** Upload your LinkedIn profile as a PDF.
2. **Profile Analysis:** The system parses and analyzes your profile, extracting skills, experience, education, and certifications.
3. **Job Data Retrieval:** Relevant job postings are fetched from the JSearch API based on your profile and location.
4. **Matching:** Your profile is matched to job postings using NLP techniques (sentence embeddings, cosine similarity) to find the best fits.

## Installation and Usage

### Prerequisites
- Python 3.8+
- A JSearch API key (set as `JSEARCH_API_KEY` in a `.env` file)

### Installation
```bash
git clone https://github.com/ckakgun/jobmatch-ai.git
cd jobmatch-ai
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

### Usage
1. Place your LinkedIn profile PDF in the `data/` directory as `linkedin_profile.pdf`.
2. Create a `.env` file in the root directory and add your JSearch API key:
   ```
   JSEARCH_API_KEY=your_api_key_here
   ```
3. Run the main script:
   ```bash
   python src/run_match.py
   ```

## Example Output

```
📍 8 jobs after filtering

🔹 Match #1
Title: Sr Data Scientist– NLP, LLM and GenAI
Company: S&P Global
Location: Washington
Description: About the Role: Grade Level (for internal use): 10 The Role: Sr Data Scientist– NLP, LLM and GenAI S&P is a leader in risk management solutions leveraging automation and AI/ML. This role is a unique opportunity for hands-on ML scientists and NLP/Gen AI/ LLM scientists to grow into the next step in their career journey...
Apply Link: https://www.indeed.com/viewjob?jk=0b59b963bb25e0ea&utm_campaign=google_jobs_apply&utm_source=google_jobs_apply&utm_medium=organic
```
...