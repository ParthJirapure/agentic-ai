"""
AI Agent for Job Recommendation - Gradio Application
Features:
- Resume Parser & Profiler (PDF / TXT upload & manual input)
- Multi-factor Hybrid Job Matching Engine with semantic similarity
- Skill Gap Analyzer with custom 30-day week-by-week learning roadmaps
- AI Career Copilot for cover letter drafting, interview drills, and resume critique
- Recruiter Job Manager for live vacancy creation
- Groq Cloud LLM / Offline Heuristic dual engine
"""

import os
import gradio as gr
from dotenv import load_dotenv

from data.jobs_data import job_manager
from agents.resume_analyzer import resume_analyzer
from agents.job_matcher import job_matcher
from agents.gap_analyzer import gap_analyzer
from agents.career_copilot import career_copilot

load_dotenv()

# Pre-packaged candidate profiles for 1-click testing
SAMPLE_PROFILES = {
    "AI & Machine Learning Engineer (Senior)": {
        "text": """Alex Chen
Email: alex.chen@ai-innovate.io | Phone: (555) 234-5678
LinkedIn: linkedin.com/in/alexchen-ai | GitHub: github.com/alexchen-ai

Senior AI & Generative Applications Engineer with 5+ years of experience engineering production LLM systems, RAG pipelines, and scalable APIs.
Education: Master of Science in Computer Science, Stanford University

Technical Skills:
Python, PyTorch, LangChain, LLMs, RAG, Vector Databases, FastAPI, Docker, Linux, Git, PostgreSQL, Scikit-Learn

Professional Experience:
Lead AI Engineer | CogniWave Systems (2022 - Present)
- Engineered enterprise Retrieval-Augmented Generation (RAG) platform with hybrid vector search.
- Fine-tuned open-source models using PyTorch, decreasing p99 inference latency by 42%.
- Built high-throughput RESTful endpoints using FastAPI and Docker.""",
        "exp": 5,
        "role": "Senior AI / LLM Applications Engineer",
        "mode": "Remote",
        "salary": 160000
    },
    "Full-Stack Web Developer (Mid-Level)": {
        "text": """Samantha Brooks
Email: samantha.b@codeworks.dev | Phone: (555) 876-5432
LinkedIn: linkedin.com/in/samanthabrooks | GitHub: github.com/samanthadev

Full-Stack Developer with 4 years of experience building modern web applications with React, TypeScript, and Python.
Education: Bachelor of Science in Software Engineering

Technical Skills:
React, TypeScript, JavaScript, Python, FastAPI, PostgreSQL, REST APIs, Tailwind CSS, Next.js, Git, HTML5, CSS3

Professional Experience:
Full-Stack Engineer | Apex Digital (2022 - Present)
- Developed responsive interactive web apps using React, Next.js, and TypeScript.
- Created microservices in Python with FastAPI and PostgreSQL with sub-100ms response times.
- Implemented modern UI components utilizing Tailwind CSS and CSS3.""",
        "exp": 4,
        "role": "Full-Stack Software Engineer (React & Python)",
        "mode": "Hybrid",
        "salary": 130000
    },
    "DevOps & Cloud Systems Architect (Senior)": {
        "text": """Marcus Vance
Email: marcus.vance@cloudscale.net | Phone: (555) 345-6789
LinkedIn: linkedin.com/in/marcusvance-devops

Senior DevOps & Infrastructure Engineer with 6+ years automating multi-region AWS and Kubernetes architectures.
Education: Bachelor of Science in Computer Engineering

Technical Skills:
AWS, Kubernetes, Terraform, Docker, CI/CD, Linux, Python, Bash, Prometheus, Grafana, Git

Professional Experience:
Senior DevOps Engineer | CloudPulse (2021 - Present)
- Orchestrated 15+ production Kubernetes clusters across multiple AWS availability zones.
- Automated complete infrastructure provisioning with Terraform and GitOps CI/CD.
- Implemented cluster-wide observability with Prometheus and Grafana dashboards.""",
        "exp": 6,
        "role": "Senior Cloud & DevOps Engineer",
        "mode": "Remote",
        "salary": 150000
    }
}

CUSTOM_CSS = """
/* Modern UI Enhancements */
@import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&family=JetBrains+Mono:wght@400;500;600&display=swap');

* {
    font-family: 'Plus Jakarta Sans', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
}

.hero-banner {
    background: linear-gradient(135deg, #0f172a 0%, #1e1b4b 45%, #312e81 80%, #4338ca 100%);
    padding: 2.2rem 2.5rem;
    border-radius: 1.25rem;
    color: #ffffff;
    box-shadow: 0 20px 25px -5px rgba(30, 27, 75, 0.4), 0 8px 10px -6px rgba(30, 27, 75, 0.3);
    margin-bottom: 1.5rem;
    border: 1px solid rgba(255, 255, 255, 0.12);
}

.hero-title {
    font-size: 2.1rem;
    font-weight: 800;
    margin: 0;
    letter-spacing: -0.025em;
    display: flex;
    align-items: center;
    gap: 0.75rem;
    color: #ffffff;
}

.hero-sub {
    font-size: 1.05rem;
    color: #c7d2fe;
    margin-top: 0.4rem;
    margin-bottom: 1.2rem;
}

.pill-tag {
    display: inline-flex;
    align-items: center;
    gap: 0.4rem;
    padding: 0.35rem 0.85rem;
    border-radius: 9999px;
    font-size: 0.82rem;
    font-weight: 600;
    background: rgba(255, 255, 255, 0.15);
    backdrop-filter: blur(8px);
    border: 1px solid rgba(255, 255, 255, 0.2);
    color: #ffffff;
}

.job-card-box {
    background: #ffffff;
    border: 1px solid #e2e8f0;
    border-radius: 1rem;
    padding: 1.5rem;
    margin-bottom: 1.2rem;
    box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.04);
}

.badge-emerald {
    background: #ecfdf5;
    color: #047857;
    border: 1px solid #a7f3d0;
    padding: 0.35rem 0.85rem;
    border-radius: 9999px;
    font-weight: 700;
    display: inline-block;
}

.badge-blue {
    background: #eff6ff;
    color: #1d4ed8;
    border: 1px solid #bfdbfe;
    padding: 0.35rem 0.85rem;
    border-radius: 9999px;
    font-weight: 700;
    display: inline-block;
}

.badge-amber {
    background: #fffbeb;
    color: #b45309;
    border: 1px solid #fde68a;
    padding: 0.35rem 0.85rem;
    border-radius: 9999px;
    font-weight: 700;
    display: inline-block;
}

.badge-purple {
    background: #faf5ff;
    color: #7e22ce;
    border: 1px solid #e9d5ff;
    padding: 0.35rem 0.85rem;
    border-radius: 9999px;
    font-weight: 700;
    display: inline-block;
}

.chip-match {
    background: #dcfce7;
    color: #166534;
    border: 1px solid #86efac;
    padding: 0.25rem 0.6rem;
    border-radius: 0.4rem;
    font-weight: 600;
    font-size: 0.82rem;
    display: inline-block;
    margin: 0.2rem;
}

.chip-gap {
    background: #fee2e2;
    color: #991b1b;
    border: 1px solid #fca5a5;
    padding: 0.25rem 0.6rem;
    border-radius: 0.4rem;
    font-weight: 600;
    font-size: 0.82rem;
    display: inline-block;
    margin: 0.2rem;
}

.chip-skill {
    background: #f1f5f9;
    color: #334155;
    border: 1px solid #cbd5e1;
    padding: 0.25rem 0.6rem;
    border-radius: 0.4rem;
    font-weight: 600;
    font-size: 0.82rem;
    display: inline-block;
    margin: 0.2rem;
}

.stat-card {
    background: #f8fafc;
    border: 1px solid #e2e8f0;
    border-radius: 0.75rem;
    padding: 1rem;
    text-align: center;
}
.stat-number {
    font-size: 1.6rem;
    font-weight: 800;
    color: #4338ca;
}
.stat-label {
    font-size: 0.75rem;
    font-weight: 700;
    color: #64748b;
    text-transform: uppercase;
    letter-spacing: 0.05em;
    margin-top: 0.25rem;
}
"""

# App Global State
DEFAULT_CANDIDATE = resume_analyzer.analyze_resume(
    resume_text=SAMPLE_PROFILES["AI & Machine Learning Engineer (Senior)"]["text"],
    preferred_role="Senior AI / LLM Applications Engineer",
    work_mode_pref="Remote",
    min_salary_pref=160000
)


def format_candidate_summary_html(profile: dict) -> str:
    """Renders sleek HTML card for the candidate profile."""
    skills = profile.get("skills", [])
    cats = profile.get("categorized_skills", {})
    contacts = profile.get("contacts", {})
    exp = profile.get("years_of_experience", 0)
    edu = profile.get("education", "Standard")

    skills_html = ""
    for cat, cat_skills in cats.items():
        chips = "".join([f'<span class="chip-skill">{s}</span>' for s in cat_skills])
        skills_html += f'<div style="margin-bottom: 0.6rem;"><div style="font-size: 0.78rem; font-weight: 700; color: #64748b; margin-bottom: 0.2rem;">{cat.upper()}</div>{chips}</div>'

    contact_bits = []
    if contacts.get("email"):
        contact_bits.append(f'📧 {contacts["email"]}')
    if contacts.get("phone"):
        contact_bits.append(f'📱 {contacts["phone"]}')
    if contacts.get("github"):
        contact_bits.append(f'🐙 GitHub')
    if contacts.get("linkedin"):
        contact_bits.append(f'🔗 LinkedIn')

    contacts_str = " &nbsp;|&nbsp; ".join(contact_bits) if contact_bits else "No direct links parsed"

    return f"""
<div style="background: #ffffff; border: 1px solid #e2e8f0; border-radius: 1rem; padding: 1.5rem; box-shadow: 0 4px 6px -1px rgba(0,0,0,0.04);">
    <div style="display: flex; justify-content: space-between; align-items: center; border-bottom: 1px solid #f1f5f9; padding-bottom: 0.75rem; margin-bottom: 1rem;">
        <div>
            <h3 style="margin: 0; font-size: 1.3rem; font-weight: 800; color: #0f172a;">Candidate Intelligence Dossier</h3>
            <div style="font-size: 0.85rem; color: #64748b; margin-top: 0.2rem;">{contacts_str}</div>
        </div>
        <div style="display: flex; gap: 0.5rem;">
            <span class="badge-blue">⏱️ {exp} Yrs Experience</span>
            <span class="badge-emerald">🎓 {edu}</span>
        </div>
    </div>
    
    <div style="display: grid; grid-template-columns: repeat(3, 1fr); gap: 0.75rem; margin-bottom: 1.2rem;">
        <div class="stat-card">
            <div class="stat-number">{len(skills)}</div>
            <div class="stat-label">Verified Skills</div>
        </div>
        <div class="stat-card">
            <div class="stat-number">{len(cats)}</div>
            <div class="stat-label">Tech Domains</div>
        </div>
        <div class="stat-card">
            <div class="stat-number">{profile.get('work_mode_preference', 'Any')}</div>
            <div class="stat-label">Work Mode Target</div>
        </div>
    </div>

    <div>
        <h4 style="margin: 0 0 0.5rem 0; font-size: 0.95rem; font-weight: 700; color: #1e293b;">Extracted Skill Inventory:</h4>
        {skills_html if skills_html else '<p style="color:#94a3b8;">No recognized skills found. Enter skills manually or paste resume text.</p>'}
    </div>
</div>
"""


def format_job_card_html(job_match: dict) -> str:
    """Format full job recommendation dossier."""
    score = job_match.get("overall_score", 0.0)
    tier = job_match.get("match_tier", "Match")
    badge_color = job_match.get("badge_color", "emerald")

    matched_req = job_match.get("matched_required_skills", [])
    missing_req = job_match.get("missing_required_skills", [])
    matched_chips = "".join([f'<span class="chip-match">✓ {s}</span>' for s in matched_req])
    missing_chips = "".join([f'<span class="chip-gap">✗ {s}</span>' for s in missing_req])

    benefits = "".join([f'<li style="margin-bottom: 0.25rem;">{b}</li>' for b in job_match.get("benefits", [])])

    return f"""
<div style="background: #ffffff; border: 1px solid #e2e8f0; border-radius: 1.1rem; padding: 1.75rem; box-shadow: 0 10px 15px -3px rgba(0,0,0,0.05); margin-top: 0.5rem;">
    <div style="display: flex; justify-content: space-between; align-items: flex-start; flex-wrap: wrap; gap: 1rem; border-bottom: 1px solid #f1f5f9; padding-bottom: 1rem; margin-bottom: 1.25rem;">
        <div>
            <div style="display: flex; align-items: center; gap: 0.6rem; margin-bottom: 0.3rem;">
                <span class="badge-{badge_color}">{tier}</span>
                <span style="font-size: 0.85rem; font-weight: 700; color: #6366f1;">{job_match.get('id')}</span>
                <span style="font-size: 0.85rem; font-weight: 600; color: #64748b;">• {job_match.get('category')}</span>
            </div>
            <h2 style="margin: 0; font-size: 1.6rem; font-weight: 800; color: #0f172a;">{job_match.get('title')}</h2>
            <div style="font-size: 1.05rem; font-weight: 600; color: #334155; margin-top: 0.25rem;">
                🏢 {job_match.get('company')} &nbsp;•&nbsp; 📍 {job_match.get('location')} ({job_match.get('work_mode')})
            </div>
        </div>
        <div style="text-align: right;">
            <div style="font-size: 2.2rem; font-weight: 800; color: #4338ca; line-height: 1;">{score:.0f}%</div>
            <div style="font-size: 0.75rem; font-weight: 700; color: #64748b; text-transform: uppercase;">Match Rating</div>
            <div style="font-size: 1.1rem; font-weight: 700; color: #059669; margin-top: 0.4rem;">{job_match.get('salary_range')}</div>
        </div>
    </div>

    <div style="display: grid; grid-template-columns: repeat(3, 1fr); gap: 0.75rem; margin-bottom: 1.4rem;">
        <div class="stat-card">
            <div class="stat-number" style="color: #059669;">{job_match.get('skill_score', 0):.0f}%</div>
            <div class="stat-label">Skill Alignment</div>
        </div>
        <div class="stat-card">
            <div class="stat-number" style="color: #2563eb;">{job_match.get('exp_score', 0):.0f}%</div>
            <div class="stat-label">Seniority Fit</div>
        </div>
        <div class="stat-card">
            <div class="stat-number" style="color: #7c3aed;">{job_match.get('pref_score', 0):.0f}%</div>
            <div class="stat-label">Preference Match</div>
        </div>
    </div>

    <div style="background: #f8fafc; border-left: 4px solid #6366f1; border-radius: 0 0.5rem 0.5rem 0; padding: 1rem 1.25rem; margin-bottom: 1.25rem;">
        <div style="font-size: 0.82rem; font-weight: 800; color: #4338ca; text-transform: uppercase; margin-bottom: 0.35rem;">
            🤖 AI Matchmaker Assessment
        </div>
        <div style="font-size: 0.95rem; color: #1e293b; line-height: 1.6;">
            {job_match.get('agent_explanation', '').replace(chr(10), '<br/>')}
        </div>
    </div>

    <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 1rem; margin-bottom: 1.25rem;">
        <div>
            <div style="font-size: 0.85rem; font-weight: 700; color: #166534; margin-bottom: 0.4rem;">
                ✓ Matched Required Skills ({len(matched_req)}):
            </div>
            <div>{matched_chips if matched_chips else '<span style="color:#94a3b8; font-size:0.85rem;">None</span>'}</div>
        </div>
        <div>
            <div style="font-size: 0.85rem; font-weight: 700; color: #991b1b; margin-bottom: 0.4rem;">
                ✗ Missing / Desired Skills ({len(missing_req)}):
            </div>
            <div>{missing_chips if missing_chips else '<span style="color:#059669; font-size:0.85rem;">✓ All core skills satisfied!</span>'}</div>
        </div>
    </div>

    <div style="border-top: 1px solid #f1f5f9; padding-top: 1rem; margin-top: 1rem;">
        <h4 style="margin: 0 0 0.4rem 0; font-size: 0.95rem; font-weight: 700; color: #1e293b;">About the Position</h4>
        <p style="font-size: 0.92rem; color: #475569; line-height: 1.5; margin: 0 0 0.75rem 0;">{job_match.get('description')}</p>
        
        <h4 style="margin: 0.75rem 0 0.3rem 0; font-size: 0.9rem; font-weight: 700; color: #1e293b;">Key Benefits & Perks:</h4>
        <ul style="margin: 0; padding-left: 1.2rem; font-size: 0.88rem; color: #475569;">
            {benefits}
        </ul>
    </div>
</div>
"""


def format_roadmap_html(gap_data: dict) -> str:
    """Format step-by-step 30-day interactive career roadmap."""
    if not gap_data:
        return "<p>Select a job to generate a personalized 30-day upskilling roadmap.</p>"

    weeks = gap_data.get("roadmap", [])
    high_roi = gap_data.get("high_roi_skill")
    resources = gap_data.get("learning_resources", [])

    weeks_html = ""
    for w in weeks:
        actions_li = "".join([f'<li style="margin-bottom: 0.3rem;">{a}</li>' for a in w.get("actions", [])])
        weeks_html += f"""
<div style="background: #ffffff; border: 1px solid #e2e8f0; border-radius: 0.85rem; padding: 1.25rem; margin-bottom: 1rem; box-shadow: 0 2px 4px rgba(0,0,0,0.03);">
    <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 0.5rem;">
        <div style="display: flex; align-items: center; gap: 0.6rem;">
            <span class="badge-blue" style="font-size: 0.82rem;">{w['week']}</span>
            <span style="font-size: 1.05rem; font-weight: 700; color: #0f172a;">{w['phase']}</span>
        </div>
        <span style="font-size: 0.82rem; font-weight: 600; color: #64748b;">⏱️ {w['time_commitment']}</span>
    </div>
    <p style="margin: 0 0 0.5rem 0; font-size: 0.9rem; color: #334155; font-weight: 600;">🎯 Goal: {w['goal']}</p>
    <ul style="margin: 0; padding-left: 1.2rem; font-size: 0.88rem; color: #475569; line-height: 1.5;">
        {actions_li}
    </ul>
</div>
"""

    res_html = "".join([
        f'<div style="margin-bottom: 0.4rem; font-size: 0.88rem;"><strong>{r["skill"]}</strong>: <span style="color: #4338ca;">{r["resource"]}</span></div>'
        for r in resources
    ])

    return f"""
<div style="background: #f8fafc; border: 1px solid #e2e8f0; border-radius: 1rem; padding: 1.5rem;">
    <div style="display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; gap: 0.8rem; margin-bottom: 1.2rem;">
        <div>
            <h3 style="margin: 0; font-size: 1.4rem; font-weight: 800; color: #0f172a;">30-Day Accelerated Upskilling Blueprint</h3>
            <div style="font-size: 0.9rem; color: #64748b;">Target Role: <strong>{gap_data.get('job_title')}</strong> at <strong>{gap_data.get('company')}</strong></div>
        </div>
        <div style="display: flex; gap: 0.6rem;">
            <span class="badge-emerald">⏱️ Est. Timeline: {gap_data.get('estimated_weeks', 3)} Weeks</span>
            {f'<span class="badge-amber">⚡ High-ROI Skill: {high_roi}</span>' if high_roi else ''}
        </div>
    </div>

    <div style="background: #e0e7ff; border-left: 4px solid #4338ca; border-radius: 0 0.5rem 0.5rem 0; padding: 0.9rem 1.1rem; margin-bottom: 1.2rem;">
        <div style="font-size: 0.8rem; font-weight: 800; color: #3730a3; text-transform: uppercase;">Recommended Capstone Showcase Project</div>
        <div style="font-size: 0.95rem; font-weight: 600; color: #1e1b4b; margin-top: 0.2rem;">{gap_data.get('capstone_project')}</div>
    </div>

    <h4 style="margin: 0 0 0.75rem 0; font-size: 1.05rem; font-weight: 700; color: #1e293b;">Weekly Milestones:</h4>
    {weeks_html}

    {f'<div style="border-top: 1px solid #e2e8f0; padding-top: 1rem; margin-top: 1rem;"><h4 style="margin: 0 0 0.5rem 0; font-size: 0.95rem; font-weight: 700; color: #1e293b;">Recommended Learning Resources:</h4>{res_html}</div>' if res_html else ''}
</div>
"""


# ==========================================
# Gradio Interface Setup
# ==========================================

with gr.Blocks(title="AI Agent for Job Recommendation") as demo:

    # State stores
    candidate_state = gr.State(DEFAULT_CANDIDATE)
    matched_jobs_state = gr.State([])
    selected_job_state = gr.State(None)

    # Hero Header
    gr.HTML("""
    <div class="hero-banner">
        <div class="hero-title">
            <span>⚡ AI Agent for Job Recommendation & Career Intelligence</span>
        </div>
        <div class="hero-sub">
            Autonomous recruitment intelligence: deep resume parsing, hybrid semantic job matching, skill gap discovery, and an interactive AI career copilot.
        </div>
        <div style="display: flex; gap: 0.6rem; flex-wrap: wrap;">
            <span class="pill-tag">✨ Groq & Heuristic Dual-Engine</span>
            <span class="pill-tag">📄 PDF & Text Resume Ingestion</span>
            <span class="pill-tag">🎯 Semantic TF-IDF & Skill Overlap</span>
            <span class="pill-tag">📈 30-Day Personalized Roadmaps</span>
            <span class="pill-tag">🤖 Tailored Cover Letters & Mock Drills</span>
        </div>
    </div>
    """)

    with gr.Tabs() as main_tabs:

        # =====================================================================
        # TAB 1: RESUME & CANDIDATE PROFILE
        # =====================================================================
        with gr.Tab("📄 Resume & Candidate Profile", id="tab_profile"):
            gr.Markdown("### 1. Ingest Your Resume or Choose a Pre-Configured Sample")

            with gr.Row():
                sample_btn_ai = gr.Button("🤖 Preset: Senior AI / LLM Engineer", size="sm", variant="secondary")
                sample_btn_web = gr.Button("💻 Preset: Mid Full-Stack Web Dev", size="sm", variant="secondary")
                sample_btn_devops = gr.Button("☁️ Preset: Senior Cloud & DevOps", size="sm", variant="secondary")

            with gr.Row():
                with gr.Column(scale=1):
                    resume_file_input = gr.File(
                        label="Upload Resume (PDF or TXT)",
                        file_types=[".pdf", ".txt", ".md"],
                        file_count="single"
                    )
                    resume_text_input = gr.Textbox(
                        label="Or Paste Resume Text / Summary Directly",
                        lines=7,
                        placeholder="Paste plain text resume or work history here...",
                        value=SAMPLE_PROFILES["AI & Machine Learning Engineer (Senior)"]["text"]
                    )
                    with gr.Accordion("Advanced Targeting & Preferences", open=True):
                        manual_skills_input = gr.Textbox(
                            label="Additional Skills (Comma-Separated)",
                            placeholder="e.g. PyTorch, Docker, Kubernetes, LangChain"
                        )
                        target_role_input = gr.Textbox(
                            label="Target Role or Title Keyword",
                            value="Senior AI / LLM Applications Engineer"
                        )
                        with gr.Row():
                            work_mode_input = gr.Dropdown(
                                label="Preferred Work Mode",
                                choices=["Any", "Remote", "Hybrid", "On-site"],
                                value="Remote"
                            )
                            min_salary_input = gr.Slider(
                                label="Minimum Desired Base Salary ($)",
                                minimum=0,
                                maximum=250000,
                                step=5000,
                                value=150000
                            )
                        manual_exp_input = gr.Slider(
                            label="Years of Experience (Leave 0 for Auto-Detection)",
                            minimum=0,
                            maximum=25,
                            step=1,
                            value=5
                        )

                    analyze_btn = gr.Button("🚀 Analyze Profile & Match Jobs", variant="primary", size="lg")

                with gr.Column(scale=1):
                    candidate_summary_display = gr.HTML(format_candidate_summary_html(DEFAULT_CANDIDATE))

        # =====================================================================
        # TAB 2: JOB RECOMMENDATIONS & EXPLORER
        # =====================================================================
        with gr.Tab("🎯 Recommended Jobs & Fit", id="tab_recommendations"):
            with gr.Row():
                filter_cat = gr.Dropdown(
                    label="Filter Category",
                    choices=job_manager.get_categories(),
                    value="All",
                    scale=1
                )
                filter_mode = gr.Dropdown(
                    label="Filter Work Mode",
                    choices=["All", "Remote", "Hybrid", "On-site"],
                    value="All",
                    scale=1
                )
                filter_min_score = gr.Slider(
                    label="Min Match Score (%)",
                    minimum=30,
                    maximum=90,
                    value=40,
                    step=5,
                    scale=1
                )
                re_match_btn = gr.Button("🔄 Refresh Recommendations", variant="secondary", scale=1)

            with gr.Row():
                with gr.Column(scale=1):
                    gr.Markdown("#### Ranked Opportunities")
                    job_selector = gr.Radio(
                        label="Select a Recommended Position to Inspect",
                        choices=[],
                        interactive=True
                    )
                with gr.Column(scale=2):
                    job_details_display = gr.HTML("<p style='padding:1rem; color:#64748b;'>Run analysis or select a job from the left to view the match dossier.</p>")
                    with gr.Row():
                        view_gap_btn = gr.Button("📈 View 30-Day Skill Gap Roadmap", variant="primary")
                        quick_cover_letter_btn = gr.Button("📝 Draft Cover Letter with AI Copilot", variant="secondary")
                        quick_interview_btn = gr.Button("🎯 Generate Mock Interview Questions", variant="secondary")

        # =====================================================================
        # TAB 3: SKILL GAP & 30-DAY ROADMAP
        # =====================================================================
        with gr.Tab("📈 Skill Gap & 30-Day Roadmap", id="tab_roadmap"):
            with gr.Row():
                roadmap_job_dropdown = gr.Dropdown(
                    label="Select Target Job for Gap Analysis",
                    choices=[],
                    interactive=True
                )
                generate_roadmap_btn = gr.Button("⚡ Re-Generate Roadmap", variant="primary")

            roadmap_display = gr.HTML("<p style='padding:1rem; color:#64748b;'>Select a target job above to build your 30-day learning plan.</p>")

        # =====================================================================
        # TAB 4: AI CAREER COPILOT & INTERVIEW COACH
        # =====================================================================
        with gr.Tab("🤖 AI Career Copilot & Interview Coach", id="tab_copilot"):
            with gr.Row():
                copilot_active_job = gr.Dropdown(
                    label="Active Context Job",
                    choices=[],
                    interactive=True
                )
            with gr.Row():
                copilot_quick_cl = gr.Button("📝 Draft Tailored Cover Letter", size="sm")
                copilot_quick_int = gr.Button("🎯 Mock Interview Prep", size="sm")
                copilot_quick_res = gr.Button("💡 Resume Critique", size="sm")
                copilot_quick_sal = gr.Button("💰 Salary Negotiation Tips", size="sm")

            chatbot = gr.Chatbot(label="AI Career Mentor", height=440)
            with gr.Row():
                chat_msg = gr.Textbox(
                    label="Message the Career Agent",
                    placeholder="Ask anything: 'What should I improve in my profile?', 'Prepare me for system design'...",
                    scale=4
                )
                chat_send_btn = gr.Button("Send", variant="primary", scale=1)
                chat_clear_btn = gr.Button("Clear", scale=1)

        # =====================================================================
        # TAB 5: JOB DATABASE & RECRUITER PORTAL
        # =====================================================================
        with gr.Tab("💼 Job Database & Recruiter Portal", id="tab_jobs"):
            gr.Markdown("### Browse All Active Positions & Post New Openings")
            with gr.Row():
                recruiter_search = gr.Textbox(label="Search Jobs (Keyword, Skill, Title)", placeholder="e.g. Python, Kubernetes, Remote...")
                recruiter_cat = gr.Dropdown(label="Category", choices=job_manager.get_categories(), value="All")
                recruiter_search_btn = gr.Button("Search", variant="secondary")

            all_jobs_display = gr.DataFrame(
                headers=["ID", "Title", "Company", "Category", "Work Mode", "Experience", "Salary Range", "Key Required Skills"],
                datatype=["str", "str", "str", "str", "str", "str", "str", "str"],
                interactive=False
            )

            with gr.Accordion("➕ Recruiter Portal: Post a New Job Opening", open=False):
                with gr.Row():
                    new_job_title = gr.Textbox(label="Job Title", placeholder="e.g. Senior MLOps Engineer")
                    new_job_company = gr.Textbox(label="Company Name", placeholder="e.g. Nova AI")
                    new_job_cat = gr.Dropdown(
                        label="Category",
                        choices=["AI & Machine Learning", "Software Development", "Cloud & DevOps", "Data & Analytics", "Cybersecurity", "Product & Design"],
                        value="AI & Machine Learning"
                    )
                with gr.Row():
                    new_job_loc = gr.Textbox(label="Location", value="Remote")
                    new_job_mode = gr.Dropdown(label="Work Mode", choices=["Remote", "Hybrid", "On-site"], value="Remote")
                    new_job_salary = gr.Textbox(label="Salary Range", value="$150,000 - $190,000")
                    new_job_min_exp = gr.Number(label="Min Years Exp", value=4)
                new_job_req_skills = gr.Textbox(label="Required Skills (comma-separated)", placeholder="e.g. Python, Docker, Kubernetes, PyTorch")
                new_job_pref_skills = gr.Textbox(label="Preferred Skills (comma-separated)", placeholder="e.g. AWS, Terraform")
                new_job_desc = gr.Textbox(label="Description", lines=3, placeholder="Describe the mission and responsibilities...")
                new_job_benefits = gr.Textbox(label="Benefits (comma-separated)", value="Health & Vision, 401(k) Match, Unlimited PTO")
                create_job_btn = gr.Button("Publish Job Opening", variant="primary")
                create_job_status = gr.Markdown("")

        # =====================================================================
        # TAB 6: SETTINGS & LLM CONFIGURATION
        # =====================================================================
        with gr.Tab("⚙️ Settings & AI Engine Config", id="tab_settings"):
            gr.Markdown("### AI Engine Configuration")
            gr.Markdown(
                "By default, this agent operates with high-precision **Local Heuristic / Semantic NLP** (TF-IDF & rule-based). "
                "You can optionally enter a **Groq API Key** to enable ultra-fast inference with Llama 3.3 / Llama 3.1 models."
            )
            with gr.Row():
                api_key_input = gr.Textbox(
                    label="Groq API Key (Optional)",
                    type="password",
                    placeholder="gsk_...",
                    value=os.getenv("GROQ_API_KEY", "")
                )
                model_selector = gr.Dropdown(
                    label="LLM Model",
                    choices=["llama-3.3-70b-versatile", "llama-3.1-8b-instant", "mixtral-8x7b-32768"],
                    value="llama-3.3-70b-versatile"
                )
            save_key_btn = gr.Button("Save & Test Engine Connection", variant="secondary")
            engine_status_msg = gr.Markdown("🟢 **Active Engine**: Intelligent Offline Heuristics + NLP (No API Key Required).")

    # ==========================================
    # Logic & Event Callbacks
    # ==========================================

    def load_preset(name: str):
        preset = SAMPLE_PROFILES[name]
        return preset["text"], preset["exp"], preset["role"], preset["mode"], preset["salary"]

    sample_btn_ai.click(
        fn=lambda: load_preset("AI & Machine Learning Engineer (Senior)"),
        outputs=[resume_text_input, manual_exp_input, target_role_input, work_mode_input, min_salary_input]
    )
    sample_btn_web.click(
        fn=lambda: load_preset("Full-Stack Web Developer (Mid-Level)"),
        outputs=[resume_text_input, manual_exp_input, target_role_input, work_mode_input, min_salary_input]
    )
    sample_btn_devops.click(
        fn=lambda: load_preset("DevOps & Cloud Systems Architect (Senior)"),
        outputs=[resume_text_input, manual_exp_input, target_role_input, work_mode_input, min_salary_input]
    )

    def analyze_and_match(
        file_obj,
        raw_text,
        manual_skills,
        target_role,
        work_mode,
        min_salary,
        manual_exp,
        cat_filter,
        mode_filter,
        min_score
    ):
        file_path = file_obj.name if file_obj else None
        profile = resume_analyzer.analyze_resume(
            resume_text=raw_text or "",
            file_path=file_path,
            manual_skills=manual_skills,
            manual_exp=manual_exp if manual_exp > 0 else None,
            preferred_role=target_role,
            work_mode_pref=work_mode,
            min_salary_pref=int(min_salary)
        )

        all_jobs = job_manager.get_all_jobs()
        matched = job_matcher.match_jobs(
            profile,
            all_jobs,
            min_match_threshold=float(min_score),
            category_filter=cat_filter,
            work_mode_filter=mode_filter
        )

        # Radio choices
        choices = [
            f"{j['id']} - {j['title']} ({j['company']}) | {j['overall_score']:.0f}% Match"
            for j in matched
        ]

        top_choice = choices[0] if choices else None
        top_job = matched[0] if matched else None
        details_html = format_job_card_html(top_job) if top_job else "<p>No matching jobs found matching your criteria.</p>"

        # Precompute roadmap for top job
        roadmap_html = format_roadmap_html(gap_analyzer.analyze_gap(profile, top_job)) if top_job else "<p>No job selected.</p>"

        profile_html = format_candidate_summary_html(profile)

        return (
            profile,
            matched,
            top_job,
            profile_html,
            gr.update(choices=choices, value=top_choice),
            details_html,
            gr.update(choices=choices, value=top_choice),
            roadmap_html,
            gr.update(choices=choices, value=top_choice)
        )

    analyze_btn.click(
        fn=analyze_and_match,
        inputs=[
            resume_file_input,
            resume_text_input,
            manual_skills_input,
            target_role_input,
            work_mode_input,
            min_salary_input,
            manual_exp_input,
            filter_cat,
            filter_mode,
            filter_min_score
        ],
        outputs=[
            candidate_state,
            matched_jobs_state,
            selected_job_state,
            candidate_summary_display,
            job_selector,
            job_details_display,
            roadmap_job_dropdown,
            roadmap_display,
            copilot_active_job
        ]
    )

    def on_job_selected(selected_str, matched_jobs):
        if not selected_str or not matched_jobs:
            return None, "<p>No job selected.</p>"
        job_id = selected_str.split(" - ")[0].strip()
        job = next((j for j in matched_jobs if j["id"] == job_id), None)
        if not job:
            return None, "<p>Job not found.</p>"
        return job, format_job_card_html(job)

    job_selector.change(
        fn=on_job_selected,
        inputs=[job_selector, matched_jobs_state],
        outputs=[selected_job_state, job_details_display]
    )

    def re_filter_matches(candidate_profile, cat, mode, min_score):
        if not candidate_profile:
            return [], gr.update(choices=[], value=None), "<p>Please analyze profile first.</p>"

        all_jobs = job_manager.get_all_jobs()
        matched = job_matcher.match_jobs(
            candidate_profile,
            all_jobs,
            min_match_threshold=float(min_score),
            category_filter=cat,
            work_mode_filter=mode
        )
        choices = [
            f"{j['id']} - {j['title']} ({j['company']}) | {j['overall_score']:.0f}% Match"
            for j in matched
        ]
        top_choice = choices[0] if choices else None
        top_job = matched[0] if matched else None
        details_html = format_job_card_html(top_job) if top_job else "<p>No matching jobs with current filters.</p>"

        return (
            matched,
            gr.update(choices=choices, value=top_choice),
            details_html,
            gr.update(choices=choices, value=top_choice),
            gr.update(choices=choices, value=top_choice)
        )

    re_match_btn.click(
        fn=re_filter_matches,
        inputs=[candidate_state, filter_cat, filter_mode, filter_min_score],
        outputs=[
            matched_jobs_state,
            job_selector,
            job_details_display,
            roadmap_job_dropdown,
            copilot_active_job
        ]
    )

    def on_roadmap_job_change(selected_str, matched_jobs, candidate_profile):
        if not selected_str or not matched_jobs:
            return "<p>Select a job to view its 30-day roadmap.</p>"
        job_id = selected_str.split(" - ")[0].strip()
        job = next((j for j in matched_jobs if j["id"] == job_id), None)
        if not job:
            job = job_manager.get_job_by_id(job_id)
        if not job:
            return "<p>Job not found.</p>"

        gap_report = gap_analyzer.analyze_gap(candidate_profile, job)
        return format_roadmap_html(gap_report)

    roadmap_job_dropdown.change(
        fn=on_roadmap_job_change,
        inputs=[roadmap_job_dropdown, matched_jobs_state, candidate_state],
        outputs=[roadmap_display]
    )
    generate_roadmap_btn.click(
        fn=on_roadmap_job_change,
        inputs=[roadmap_job_dropdown, matched_jobs_state, candidate_state],
        outputs=[roadmap_display]
    )

    # Copilot Chat handlers
    def copilot_chat_handler(message, history, candidate_profile, selected_str, matched_jobs, api_key, model):
        if not message.strip():
            return "", history

        job = None
        if selected_str and matched_jobs:
            job_id = selected_str.split(" - ")[0].strip()
            job = next((j for j in matched_jobs if j["id"] == job_id), None)

        bot_reply = career_copilot.chat_response(
            message=message,
            chat_history=history or [],
            candidate_profile=candidate_profile or DEFAULT_CANDIDATE,
            current_job=job,
            api_key=api_key,
            model=model
        )

        history = history or []
        history.append({"role": "user", "content": message})
        history.append({"role": "assistant", "content": bot_reply})
        return "", history

    chat_send_btn.click(
        fn=copilot_chat_handler,
        inputs=[chat_msg, chatbot, candidate_state, copilot_active_job, matched_jobs_state, api_key_input, model_selector],
        outputs=[chat_msg, chatbot]
    )
    chat_msg.submit(
        fn=copilot_chat_handler,
        inputs=[chat_msg, chatbot, candidate_state, copilot_active_job, matched_jobs_state, api_key_input, model_selector],
        outputs=[chat_msg, chatbot]
    )
    chat_clear_btn.click(fn=lambda: [], outputs=[chatbot])

    # Quick prompt actions
    def trigger_quick_action(action_type, candidate_profile, selected_str, matched_jobs, history, api_key, model):
        job = None
        if selected_str and matched_jobs:
            job_id = selected_str.split(" - ")[0].strip()
            job = next((j for j in matched_jobs if j["id"] == job_id), None)

        history = history or []

        if action_type == "cover_letter":
            user_msg = f"Please draft a tailored cover letter for {job['title'] if job else 'my target job'}."
            reply = career_copilot.generate_cover_letter(candidate_profile or DEFAULT_CANDIDATE, job or job_manager.get_all_jobs()[0], api_key, model)
        elif action_type == "interview":
            user_msg = f"Generate mock interview questions and answer strategy for {job['title'] if job else 'this role'}."
            reply = career_copilot.generate_interview_prep(candidate_profile or DEFAULT_CANDIDATE, job or job_manager.get_all_jobs()[0], api_key, model)
        elif action_type == "resume":
            user_msg = f"How should I optimize my resume specifically for {job['title'] if job else 'this position'}?"
            reply = career_copilot.critique_resume(candidate_profile or DEFAULT_CANDIDATE, job or job_manager.get_all_jobs()[0])
        elif action_type == "salary":
            user_msg = "What are the best salary negotiation tactics for this position?"
            reply = career_copilot.chat_response("salary negotiation tactics", history, candidate_profile or DEFAULT_CANDIDATE, job, api_key, model)
        else:
            return history

        history.append({"role": "user", "content": user_msg})
        history.append({"role": "assistant", "content": reply})
        return history

    copilot_quick_cl.click(
        fn=lambda c, s, m, h, k, mod: trigger_quick_action("cover_letter", c, s, m, h, k, mod),
        inputs=[candidate_state, copilot_active_job, matched_jobs_state, chatbot, api_key_input, model_selector],
        outputs=[chatbot]
    )
    copilot_quick_int.click(
        fn=lambda c, s, m, h, k, mod: trigger_quick_action("interview", c, s, m, h, k, mod),
        inputs=[candidate_state, copilot_active_job, matched_jobs_state, chatbot, api_key_input, model_selector],
        outputs=[chatbot]
    )
    copilot_quick_res.click(
        fn=lambda c, s, m, h, k, mod: trigger_quick_action("resume", c, s, m, h, k, mod),
        inputs=[candidate_state, copilot_active_job, matched_jobs_state, chatbot, api_key_input, model_selector],
        outputs=[chatbot]
    )
    copilot_quick_sal.click(
        fn=lambda c, s, m, h, k, mod: trigger_quick_action("salary", c, s, m, h, k, mod),
        inputs=[candidate_state, copilot_active_job, matched_jobs_state, chatbot, api_key_input, model_selector],
        outputs=[chatbot]
    )

    # Tab 5: Job Explorer and Recruiter Actions
    def load_all_jobs_table(query, cat):
        jobs = job_manager.filter_jobs(category=cat, query=query)
        rows = []
        for j in jobs:
            rows.append([
                j.get("id"),
                j.get("title"),
                j.get("company"),
                j.get("category"),
                j.get("work_mode"),
                f"{j.get('min_years_exp', 0)}+ yrs",
                j.get("salary_range"),
                ", ".join(j.get("required_skills", [])[:4])
            ])
        return rows

    recruiter_search_btn.click(
        fn=load_all_jobs_table,
        inputs=[recruiter_search, recruiter_cat],
        outputs=[all_jobs_display]
    )

    def create_new_job(title, company, cat, loc, mode, salary, min_exp, req_s, pref_s, desc, ben):
        if not title or not company:
            return "⚠️ Error: Title and Company Name are required.", load_all_jobs_table("", "All")

        job_dict = {
            "title": title.strip(),
            "company": company.strip(),
            "category": cat,
            "location": loc.strip(),
            "work_mode": mode,
            "salary_range": salary.strip(),
            "min_salary": 100000,
            "min_years_exp": int(min_exp),
            "required_skills": req_s,
            "preferred_skills": pref_s,
            "description": desc.strip(),
            "benefits": ben
        }
        added = job_manager.add_job(job_dict)
        return f"✅ Successfully added **{added['title']}** at **{added['company']}** (ID: {added['id']})! Candidates can now match with it.", load_all_jobs_table("", "All")

    create_job_btn.click(
        fn=create_new_job,
        inputs=[
            new_job_title,
            new_job_company,
            new_job_cat,
            new_job_loc,
            new_job_mode,
            new_job_salary,
            new_job_min_exp,
            new_job_req_skills,
            new_job_pref_skills,
            new_job_desc,
            new_job_benefits
        ],
        outputs=[create_job_status, all_jobs_display]
    )

    # Tab 6: Settings test
    def test_engine_connection(key, model):
        if not key or not key.strip():
            return "🟢 **Active Engine**: Intelligent Offline Heuristic Agent (TF-IDF + Taxonomy + Heuristics). All features fully operational!"
        try:
            from groq import Groq
            client = Groq(api_key=key.strip())
            resp = client.chat.completions.create(
                model=model,
                messages=[{"role": "user", "content": "Ping"}],
                max_tokens=5
            )
            return f"🚀 **Active Engine**: Groq Cloud LLM Connected! Model: `{model}`. Live AI responses active."
        except Exception as e:
            return f"⚠️ **Groq Connection Failed**: {str(e)}. Falling back safely to Offline Intelligent Heuristic Agent."

    save_key_btn.click(
        fn=test_engine_connection,
        inputs=[api_key_input, model_selector],
        outputs=[engine_status_msg]
    )

    # Initial page load data
    demo.load(
        fn=lambda: (
            load_all_jobs_table("", "All"),
            *analyze_and_match(
                None,
                SAMPLE_PROFILES["AI & Machine Learning Engineer (Senior)"]["text"],
                "",
                "Senior AI / LLM Applications Engineer",
                "Remote",
                160000,
                5,
                "All",
                "All",
                40
            )
        ),
        outputs=[
            all_jobs_display,
            candidate_state,
            matched_jobs_state,
            selected_job_state,
            candidate_summary_display,
            job_selector,
            job_details_display,
            roadmap_job_dropdown,
            roadmap_display,
            copilot_active_job
        ]
    )


if __name__ == "__main__":
    demo.launch(
        inbrowser=True,
        share=False,
        css=CUSTOM_CSS,
        theme=gr.themes.Soft(primary_hue="indigo")
    )
