# ⚡ AI Agent for Job Recommendation & Career Intelligence

An autonomous, multi-agent recruitment and career acceleration platform powered by **Gradio 6**, **scikit-learn**, and optional **Groq Cloud LLM** (`llama-3.3-70b-versatile`).

---

## 🌟 Key Features

### 1. 📄 Intelligent Resume & Profile Ingestion
- **Multi-Format Support**: Upload PDF or plain text (`.txt`, `.md`) resumes, or paste text directly.
- **Skill Extraction**: Identifies 100+ modern technical skills, frameworks, cloud tooling, and methodologies.
- **Automated Intelligence**: Automatically detects years of experience, highest education credential, contact coordinates, and technical domain breakdown.
- **1-Click Presets**: Test instantly with pre-loaded profiles for Senior AI Engineers, Mid-Level Full-Stack Developers, and Cloud/DevOps Specialists.

### 2. 🎯 Hybrid Multi-Factor Recommendation Engine
- **Skill Synergy (50%)**: Combines Jaccard set overlap with TF-IDF cosine semantic similarity for deep context awareness.
- **Seniority Curve (25%)**: Evaluates candidate experience versus job requirements with non-linear scoring.
- **Preference Alignment (25%)**: Factors in work mode (Remote, Hybrid, On-site), salary floors, and target job titles.
- **Explainable Match Dossier**: Generates natural language recruiter justifications ("Why You Match") alongside color-coded matched and missing skill chips.

### 3. 📈 Skill Gap Discovery & 30-Day Accelerated Roadmap
- **Delta Analysis**: Differentiates between critical required skills vs nice-to-have preferred skills.
- **High-ROI Skill Highlight**: Identifies the single skill with the highest immediate impact on match percentage and compensation.
- **4-Week Structured Blueprint**:
  - *Week 1*: Foundations & Architecture
  - *Week 2*: Intermediate Hands-on Tooling
  - *Week 3*: Custom Capstone Portfolio Project
  - *Week 4*: Technical Interview Preparation & Resume Alignment
- **Curated Resources**: Direct mappings to official documentation, courses, and certifications.

### 4. 🤖 AI Career Copilot & Interview Coach
- **Tailored Cover Letter Generator**: Generates high-converting, professional cover letters tailored to any selected position.
- **Mock Interview Simulator**: Provides technical deep-dive questions, behavioral STAR prompts, and golden candidate questions.
- **Resume Optimizer**: Suggests concrete metric-driven bullet point enhancements.
- **Interactive Chat**: Ask questions regarding compensation negotiation, career pivots, and system design.

### 5. 💼 Job Explorer & Recruiter Portal
- Browse 15+ built-in realistic job postings across AI/ML, Fullstack, Cloud/DevOps, Data, and Cybersecurity.
- Live job posting form allows recruiters to publish new positions that candidates can immediately match against.

### 6. ⚙️ Dual-Engine Architecture
- **Offline Heuristic Agent (Zero-Setup)**: Works 100% locally out-of-the-box using TF-IDF, taxonomy heuristics, and regex matching. No API key needed.
- **Groq Cloud LLM (Optional)**: Connect a free Groq API key in the Settings tab to unleash ultra-fast reasoning with `llama-3.3-70b-versatile` or `llama-3.1-8b-instant`.

---

## 🏗️ Architecture & Directory Structure

```
flexi/
├── app.py                      # Main Gradio 6 web application & UI
├── requirements.txt            # Dependency list
├── README.md                   # Project documentation
├── sample_resume.txt           # Sample candidate resume for testing
├── data/
│   └── jobs_data.py            # Curated job listings database & JobManager
├── agents/
│   ├── resume_analyzer.py      # Resume text extractor & skill classifier
│   ├── job_matcher.py          # Multi-factor hybrid matching engine
│   ├── gap_analyzer.py         # Skill gap & 30-day roadmap generator
│   └── career_copilot.py       # Conversational AI coach & document drafter
└── tests/
    └── test_agents.py          # Automated unit test suite
```

---

## 🚀 Quick Start Guide

### 1. Installation

Ensure Python 3.10+ is installed:

```bash
pip install -r requirements.txt
```

### 2. Launch Application

Run the Gradio interface:

```bash
python app.py
```

The app will launch locally at `http://127.0.0.1:7860`.

### 3. Run Automated Tests

Execute the unit test suite:

```bash
python -m unittest tests/test_agents.py
```

---

## 🔑 Groq LLM Configuration (Optional)

To enable live LLM generation for cover letters, interview coaching, and career chat:
1. Obtain an API key from [Groq Console](https://console.groq.com/).
2. Either create a `.env` file in the project root:
   ```env
   GROQ_API_KEY=gsk_your_api_key_here
   ```
   Or paste it directly into the **Settings & AI Engine Config** tab inside the web UI.
