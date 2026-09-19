"""
AI Career Copilot Agent
Provides interactive career guidance, tailored cover letter generation, mock interview
preparation, and resume critique. Works offline with high-quality heuristics and supports
Groq LLMs (Llama 3.3 70B / Llama 3.1 8B) when an API key is available.
"""

import os
from typing import Dict, List, Any, Optional

try:
    from groq import Groq
except ImportError:
    Groq = None


class CareerCopilotAgent:
    """Conversational AI career mentor and application strategist."""

    def __init__(self):
        self.default_model = "llama-3.3-70b-versatile"

    def _get_groq_client(self, api_key: Optional[str] = None):
        """Retrieve configured Groq client if key is present."""
        key = api_key or os.getenv("GROQ_API_KEY")
        if key and Groq is not None:
            try:
                return Groq(api_key=key.strip())
            except Exception:
                return None
        return None

    def generate_cover_letter(
        self,
        candidate_profile: Dict[str, Any],
        job: Dict[str, Any],
        api_key: Optional[str] = None,
        model: Optional[str] = None
    ) -> str:
        """Draft an impactful, tailored cover letter for a specific position."""
        client = self._get_groq_client(api_key)
        skills = candidate_profile.get("skills", ["Software Engineering"])
        top_skills = ", ".join(skills[:5])
        exp = candidate_profile.get("years_of_experience", 3)
        job_title = job.get("title", "Software Engineer")
        company = job.get("company", "Innovative Tech Co")
        req_skills = ", ".join(job.get("required_skills", []))

        if client:
            try:
                prompt = f"""
You are an expert executive career coach. Write a tailored, persuasive, and professional cover letter.
Candidate Details:
- Years of Experience: {exp} years
- Key Skills: {top_skills}
- Contact Email: {candidate_profile.get('contacts', {}).get('email', '[Email Address]')}

Target Role:
- Title: {job_title}
- Company: {company}
- Location: {job.get('location', 'Remote')}
- Key Requirements: {req_skills}
- Job Description Context: {job.get('description', '')}

Requirements:
- Strong, engaging opening hook expressing excitement for {company}.
- 2 structured body paragraphs connecting candidate's {top_skills} to company needs with quantifiable framing.
- Professional closing call-to-action.
- Tone: confident, authentic, and modern. Do not use generic filler phrases.
"""
                resp = client.chat.completions.create(
                    model=model or self.default_model,
                    messages=[{"role": "user", "content": prompt}],
                    temperature=0.7,
                    max_tokens=800
                )
                return resp.choices[0].message.content.strip()
            except Exception as e:
                pass  # Gracefully fallback to heuristic template

        # Heuristic Template Fallback
        matched_str = top_skills if top_skills else "modern software engineering best practices"
        return f"""Dear Hiring Team at {company},

I am writing to express my enthusiastic interest in the {job_title} position at {company}. With over {exp} years of hands-on experience building scalable applications and deep familiarity with {matched_str}, I am confident in my ability to deliver immediate value to your team.

Throughout my career, I have focused on engineering resilient systems and driving measurable results. At {company}, your commitment to technical excellence and solving impactful problems resonates strongly with my professional values. My technical background in {top_skills} aligns seamlessly with your need for someone who can navigate {req_skills}.

What excites me most about {company} is the opportunity to contribute directly to your ongoing technical initiatives. I pride myself on clean architecture, collaborative problem-solving, and continuous learning. I welcome the opportunity to discuss how my skill set and proactive approach can support your upcoming milestones.

Thank you for your time and consideration. I look forward to the possibility of an interview.

Sincerely,
[Candidate Name]
{candidate_profile.get('contacts', {}).get('email', 'candidate@example.com')}
{candidate_profile.get('contacts', {}).get('phone', '+1 (555) 019-2834')}
{candidate_profile.get('contacts', {}).get('linkedin', 'linkedin.com/in/candidate')}"""

    def generate_interview_prep(
        self,
        candidate_profile: Dict[str, Any],
        job: Dict[str, Any],
        api_key: Optional[str] = None,
        model: Optional[str] = None
    ) -> str:
        """Generate tailored interview prep questions with model answers and strategies."""
        client = self._get_groq_client(api_key)
        job_title = job.get("title", "Position")
        company = job.get("company", "Company")
        req_skills = job.get("required_skills", [])
        top_skills = req_skills[:4] if req_skills else ["System Design", "Python"]

        if client:
            try:
                prompt = f"""
You are a Principal Tech Interviewer at a top technology company.
Generate an intensive interview preparation guide for a candidate interviewing for:
- Role: {job_title} at {company}
- Core Skills Required: {', '.join(req_skills)}
- Candidate Skills: {', '.join(candidate_profile.get('skills', []))}
- Candidate Experience: {candidate_profile.get('years_of_experience', 3)} years

Include:
1. 2 Technical Deep-Dive Questions specifically testing {', '.join(top_skills[:2])}, with what the interviewer looks for and key concepts to mention.
2. 1 Architecture / System Design Scenario relevant to this role.
3. 2 Behavioral / Situational Questions utilizing the STAR method (Situation, Task, Action, Result).
4. 3 High-leverage questions the candidate should ask the interviewer to stand out.
Format cleanly with Markdown headers and bullet points.
"""
                resp = client.chat.completions.create(
                    model=model or self.default_model,
                    messages=[{"role": "user", "content": prompt}],
                    temperature=0.6,
                    max_tokens=1000
                )
                return resp.choices[0].message.content.strip()
            except Exception:
                pass

        # Heuristic Template Fallback
        s1 = top_skills[0] if len(top_skills) > 0 else "Python"
        s2 = top_skills[1] if len(top_skills) > 1 else "Cloud Architecture"

        return f"""# 🎯 Interview Preparation Guide: {job_title} ({company})

### 1. Technical Deep-Dive Questions

#### Q1: Core Mastery in {s1}
- **Question**: "Can you walk us through a challenging production issue you encountered while implementing {s1}, how you diagnosed root cause, and how you ensured it wouldn't happen again?"
- **Interviewer's Goal**: Evaluating diagnostic depth, observability practices, and operational maturity.
- **Key Concepts to Mention**: Profiling tools, latency monitoring, defensive programming, and post-mortem documentation.

#### Q2: Practical Architecture with {s2}
- **Question**: "When architecting a solution involving {s2}, what trade-offs do you evaluate regarding consistency, availability, and developer velocity?"
- **Interviewer's Goal**: Gauging architectural maturity and understanding of real-world constraints.
- **Answer Tip**: Use concrete metrics (e.g., p99 latency, cost implications, fault tolerance).

---

### 2. Behavioral & Leadership (STAR Method)

#### Q3: Cross-Functional Ambiguity
- **Question**: "Describe a time when engineering requirements were underspecified or rapidly changing. How did you prioritize deliverables?"
- **STAR Framing**:
  - *Situation*: Project scope was shifting weekly.
  - *Task*: Needed to align product and engineering on an MVP milestone.
  - *Action*: Established asynchronous design RFCs and quick sprint retrospectives.
  - *Result*: Delivered core functionality 10% ahead of deadline.

#### Q4: Technical Conflict Resolution
- **Question**: "Tell me about a technical disagreement you had with a peer or tech lead. How did you reach resolution?"
- **Focus**: Data-driven decisions, prototyping POCs, and egoless collaboration.

---

### 3. Golden Questions to Ask the Hiring Team
1. *"What does success look like for this {job_title} in the first 90 days?"*
2. *"What is the biggest technical debt or scaling bottleneck currently facing your team?"*
3. *"How does engineering influence the quarterly product roadmap at {company}?"*"""

    def critique_resume(self, candidate_profile: Dict[str, Any], job: Dict[str, Any]) -> str:
        """Provide concrete, high-impact resume enhancement recommendations."""
        skills = candidate_profile.get("skills", [])
        missing_req = [s for s in job.get("required_skills", []) if s.lower() not in {k.lower() for k in skills}]

        tips = [
            "### 💡 Strategic Resume Optimization Advice",
            f"Targeting: **{job.get('title')}** at **{job.get('company')}**\n",
            "#### 1. Quantify Your Impact (Google XYZ Formula)",
            "- Transform bullets from *'Worked on API services'* to: *'Architected 4 REST endpoints using FastAPI, decreasing average p95 response times by 38% for 50k daily active users.'*",
            "- Ensure at least 60% of bullet points contain a number, percentage, or currency figure.\n",
            "#### 2. ATS Keyword Alignment",
        ]

        if missing_req:
            tips.append(f"- **Critical ATS Keywords to integrate**: Incorporate `{', '.join(missing_req[:4])}` into your skills section or relevant project bullet points.")
        else:
            tips.append("- **ATS Match**: Your resume already matches all key ATS technical terms for this role!")

        tips.extend([
            "\n#### 3. Lead With Relevant Seniority",
            f"- Your profile reflects ~{candidate_profile.get('years_of_experience', 2)} years of experience. Ensure your summary statement directly addresses the requirements of a **{job.get('title')}**.",
            "- Move your strongest tech stack keywords into the top third of your resume for maximum recruiter scan speed (recruiters scan in ~6 seconds)."
        ])

        return "\n".join(tips)

    def chat_response(
        self,
        message: str,
        chat_history: List[Dict[str, str]],
        candidate_profile: Dict[str, Any],
        current_job: Optional[Dict[str, Any]],
        api_key: Optional[str] = None,
        model: Optional[str] = None
    ) -> str:
        """Answer free-form candidate inquiries as an AI Career Agent."""
        client = self._get_groq_client(api_key)
        skills = candidate_profile.get("skills", [])
        exp = candidate_profile.get("years_of_experience", 2)
        job_ctx = f"Currently reviewing job: {current_job.get('title')} at {current_job.get('company')}" if current_job else "No specific job selected yet."

        if client:
            try:
                system_prompt = f"""You are an elite AI Career Coach and Job Recruiter.
Candidate Profile:
- Skills: {', '.join(skills)}
- Experience: {exp} years
- Active Job Context: {job_ctx}

Provide actionable, supportive, concise, and pragmatic advice. Format answers using markdown lists and bold headers when helpful. Avoid empty fluff."""

                messages = [{"role": "system", "content": system_prompt}]
                for entry in chat_history[-6:]:
                    messages.append({"role": entry.get("role", "user"), "content": entry.get("content", "")})
                messages.append({"role": "user", "content": message})

                resp = client.chat.completions.create(
                    model=model or self.default_model,
                    messages=messages,
                    temperature=0.7,
                    max_tokens=700
                )
                return resp.choices[0].message.content.strip()
            except Exception as e:
                pass

        # Offline Intelligent Heuristic Response Router
        msg_lower = message.lower()
        if "cover letter" in msg_lower:
            if current_job:
                return self.generate_cover_letter(candidate_profile, current_job)
            return "Please select a recommended job from the Recommendations tab first so I can tailor the cover letter specifically to that company and position!"

        elif "interview" in msg_lower or "question" in msg_lower:
            if current_job:
                return self.generate_interview_prep(candidate_profile, current_job)
            return "Select any recommended job card to unlock tailored technical and behavioral mock interview drills!"

        elif "resume" in msg_lower or "improve" in msg_lower or "cv" in msg_lower:
            if current_job:
                return self.critique_resume(candidate_profile, current_job)
            return f"Based on your profile with {len(skills)} skills and ~{exp} years of experience, the biggest boost comes from adding metrics (e.g. latency, cost, user adoption) to your bullet points. Select a specific job for tailored ATS keyword tips!"

        elif "salary" in msg_lower or "negotiat" in msg_lower:
            salary_ctx = current_job.get('salary_range', '$130k - $170k') if current_job else 'the market benchmark'
            return f"""### 💰 Compensation & Negotiation Strategy
Targeting {salary_ctx}:
1. **Never Give the First Number**: When asked for your expectations, respond: *"I'm focused on finding the right role fit and trust you offer competitive compensation aligned with current market data. What is the approved range for this position?"*
2. **Anchor at the Top Decile**: If forced to state a range, base your lower bound on the median target and the upper bound 15-20% higher.
3. **Total Compensation View**: Remember to evaluate base salary, annual bonus, equity vesting schedules, 401(k) match, and flexible remote stipends."""

        else:
            return f"""Hello! I am your **AI Career Copilot**.
I am currently factoring in your profile:
- **Skills**: {', '.join(skills[:6]) if skills else 'General Tech'}
- **Seniority**: ~{exp} years of experience
- **Target Role**: {current_job.get('title') if current_job else 'Select a job to dive deeper'}

**You can ask me to:**
- *"Draft a tailored cover letter for this role"*
- *"Run a mock interview with technical questions"*
- *"Suggest 30-day projects to bridge missing skills"*
- *"Give me resume revision tips for this job"*"""


# Singleton instance
career_copilot = CareerCopilotAgent()
