"""
Job Database and Management for AI Job Recommendation Agent.
Contains curated realistic job listings across multiple domains and utility functions.
"""

from typing import List, Dict, Any, Optional

DEFAULT_JOBS: List[Dict[str, Any]] = [
    {
        "id": "JOB-001",
        "title": "Senior AI / LLM Applications Engineer",
        "company": "CognitiveLabs AI",
        "location": "San Francisco, CA",
        "work_mode": "Remote",
        "experience_level": "Senior (5-8 yrs)",
        "min_years_exp": 5,
        "salary_range": "$160,000 - $210,000",
        "min_salary": 160000,
        "category": "AI & Machine Learning",
        "required_skills": ["Python", "PyTorch", "LangChain", "LLMs", "RAG", "Vector Databases", "FastAPI"],
        "preferred_skills": ["Docker", "Kubernetes", "LlamaIndex", "Fine-tuning", "vLLM", "AWS"],
        "description": "Lead the development of production-grade generative AI pipelines and autonomous agents. Architect Retrieval-Augmented Generation (RAG) systems and fine-tune open-weight models for enterprise automation.",
        "benefits": ["Equity / Stock Options", "Unlimited PTO", "Home Office Stipend", "$3,000 Annual Learning Budget"]
    },
    {
        "id": "JOB-002",
        "title": "Machine Learning Engineer (Computer Vision & Audio)",
        "company": "NeuralVision Robotics",
        "location": "Boston, MA",
        "work_mode": "Hybrid",
        "experience_level": "Mid-Level (3-5 yrs)",
        "min_years_exp": 3,
        "salary_range": "$135,000 - $170,000",
        "min_salary": 135000,
        "category": "AI & Machine Learning",
        "required_skills": ["Python", "OpenCV", "PyTorch", "TensorFlow", "Deep Learning", "NumPy", "C++"],
        "preferred_skills": ["CUDA", "ONNX", "Edge AI", "ROS2", "Linux"],
        "description": "Design and optimize real-time neural network models for autonomous robotic perception and edge processing. Deploy low-latency vision algorithms onto NVIDIA Jetson hardware.",
        "benefits": ["Full Health/Dental/Vision", "401(k) 6% Match", "Relocation Assistance", "Annual Bonus"]
    },
    {
        "id": "JOB-003",
        "title": "Full-Stack Software Engineer (React & Python)",
        "company": "FinFlow Technologies",
        "location": "New York, NY",
        "work_mode": "Hybrid",
        "experience_level": "Mid-Level (3-5 yrs)",
        "min_years_exp": 3,
        "salary_range": "$130,000 - $165,000",
        "min_salary": 130000,
        "category": "Software Development",
        "required_skills": ["Python", "FastAPI", "React", "TypeScript", "PostgreSQL", "REST APIs", "Tailwind CSS"],
        "preferred_skills": ["Next.js", "Docker", "Redis", "GraphQL", "AWS"],
        "description": "Develop high-throughput financial web applications. Build responsive, real-time analytics interfaces with React and secure, performant backends with FastAPI and PostgreSQL.",
        "benefits": ["Gym Membership", "Hybrid Schedule (2 days WFH)", "Generous Bonus", "Top-tier Medical Coverage"]
    },
    {
        "id": "JOB-004",
        "title": "Senior Cloud & DevOps Engineer",
        "company": "ScalePulse Cloud Systems",
        "location": "Austin, TX",
        "work_mode": "Remote",
        "experience_level": "Senior (5-8 yrs)",
        "min_years_exp": 6,
        "salary_range": "$150,000 - $190,000",
        "min_salary": 150000,
        "category": "Cloud & DevOps",
        "required_skills": ["AWS", "Kubernetes", "Terraform", "Docker", "CI/CD", "Linux", "Python", "Bash"],
        "preferred_skills": ["Helm", "Prometheus", "Grafana", "ArgoCD", "GCP", "Ansible"],
        "description": "Architect and automate cloud infrastructure spanning multiple regions. Build resilient GitOps CI/CD pipelines, optimize cloud expenditure, and uphold 99.99% service uptime.",
        "benefits": ["100% Remote flexibility", "Flexible working hours", "Comprehensive Medical/Life Insurance", "Latest MacBook Pro"]
    },
    {
        "id": "JOB-005",
        "title": "Staff Backend Engineer (Distributed Systems)",
        "company": "Nexus Stream Data",
        "location": "Seattle, WA",
        "work_mode": "Hybrid",
        "experience_level": "Lead / Principal (8+ yrs)",
        "min_years_exp": 8,
        "salary_range": "$190,000 - $250,000",
        "min_salary": 190000,
        "category": "Software Development",
        "required_skills": ["Go", "Distributed Systems", "Kafka", "PostgreSQL", "gRPC", "Microservices", "Docker"],
        "preferred_skills": ["Cassandra", "Kubernetes", "Redis", "Rust", "System Architecture"],
        "description": "Drive architecture for ultra-high throughput event ingestion engines processing billions of daily events. Mentor senior engineering staff and guide technical direction.",
        "benefits": ["Substantial Equity Grant", "Wellness Allowance", "Executive Mentorship", "Annual Sabbatical Program"]
    },
    {
        "id": "JOB-006",
        "title": "Lead Data Scientist & Analytics Specialist",
        "company": "Aura Commerce",
        "location": "Chicago, IL",
        "work_mode": "Remote",
        "experience_level": "Senior (5-8 yrs)",
        "min_years_exp": 5,
        "salary_range": "$145,000 - $185,000",
        "min_salary": 145000,
        "category": "Data & Analytics",
        "required_skills": ["Python", "SQL", "Machine Learning", "Pandas", "Scikit-Learn", "A/B Testing", "Tableau"],
        "preferred_skills": ["Snowflake", "dbt", "Statistical Modeling", "Airflow", "Customer Lifetime Value"],
        "description": "Extract predictive insights from massive consumer datasets. Lead experimentation frameworks, design recommendation systems, and deliver high-stakes executive analytical briefings.",
        "benefits": ["Work from anywhere", "Parental Leave (16 weeks)", "Cellular / Internet Reimbursement", "401(k) Match"]
    },
    {
        "id": "JOB-007",
        "title": "Cybersecurity & DevSecOps Engineer",
        "company": "Fortress Shield Defense",
        "location": "Washington, DC",
        "work_mode": "Hybrid",
        "experience_level": "Mid-Level (3-5 yrs)",
        "min_years_exp": 4,
        "salary_range": "$135,000 - $175,000",
        "min_salary": 135000,
        "category": "Cybersecurity",
        "required_skills": ["Cybersecurity", "Network Security", "Penetration Testing", "Python", "Linux", "SIEM", "Cloud Security"],
        "preferred_skills": ["AWS Security", "CISSP", "Docker Security", "Splunk", "Incident Response"],
        "description": "Defend cloud-native microservice architectures against zero-day exploits. Embed security automation (SAST/DAST) into CI/CD workflows and coordinate vulnerability remediation.",
        "benefits": ["Security Clearance Sponsorship", "Annual Tech Conference Pass", "Health & Vision", "Tuition Reimbursement"]
    },
    {
        "id": "JOB-008",
        "title": "Senior Product Manager (AI Platform)",
        "company": "Synapse Product Group",
        "location": "San Francisco, CA",
        "work_mode": "Remote",
        "experience_level": "Senior (5-8 yrs)",
        "min_years_exp": 5,
        "salary_range": "$155,000 - $205,000",
        "min_salary": 155000,
        "category": "Product & Design",
        "required_skills": ["Product Management", "AI/ML Concepts", "Agile", "User Research", "Roadmapping", "Data Analysis", "SQL"],
        "preferred_skills": ["LLM Applications", "System Design Understanding", "Jira", "Figma", "Go-To-Market"],
        "description": "Define product vision and strategic execution for our next-gen developer AI agent platform. Bridge business priorities with technical feasibility alongside elite ML engineering teams.",
        "benefits": ["Competitive Equity", "Annual Company Retreats", "Comprehensive Health Benefits", "Home Workspace Budget"]
    },
    {
        "id": "JOB-009",
        "title": "Junior Python & Data Automation Developer",
        "company": "AutomateIQ Solutions",
        "location": "Remote",
        "work_mode": "Remote",
        "experience_level": "Junior (0-2 yrs)",
        "min_years_exp": 1,
        "salary_range": "$75,000 - $95,000",
        "min_salary": 75000,
        "category": "Software Development",
        "required_skills": ["Python", "SQL", "Pandas", "Git", "REST APIs", "Data Scraping"],
        "preferred_skills": ["Flask", "FastAPI", "Selenium", "PostgreSQL", "Docker Basics"],
        "description": "Ideal entry-to-mid career opportunity to build automated ETL pipelines, web scrapers, and data quality check systems. Learn under direct guidance of principal architects.",
        "benefits": ["Dedicated Career Mentorship", "Flexible Hours", "Learning & Development Stipend", "Equipment Provided"]
    },
    {
        "id": "JOB-010",
        "title": "Principal UI/UX Designer & Design Systems Lead",
        "company": "Vivid Studio Interactive",
        "location": "Los Angeles, CA",
        "work_mode": "Hybrid",
        "experience_level": "Senior (5-8 yrs)",
        "min_years_exp": 6,
        "salary_range": "$140,000 - $180,000",
        "min_salary": 140000,
        "category": "Product & Design",
        "required_skills": ["Figma", "UI Design", "UX Research", "Design Systems", "Prototyping", "Wireframing"],
        "preferred_skills": ["HTML/CSS", "Design Tokens", "Accessibility (WCAG)", "Motion Design", "User Testing"],
        "description": "Direct user experience strategy across our flagship consumer web and mobile apps. Build and scale accessible, stunning design systems used by hundreds of engineers.",
        "benefits": ["Flexible Hybrid Work", "Annual Creative Stipend", "401(k) Matching", "Full Healthcare Coverage"]
    },
    {
        "id": "JOB-011",
        "title": "Senior Data Engineer (Snowflake & Spark)",
        "company": "OmniData Analytics",
        "location": "Dallas, TX",
        "work_mode": "Remote",
        "experience_level": "Senior (5-8 yrs)",
        "min_years_exp": 5,
        "salary_range": "$145,000 - $185,000",
        "min_salary": 145000,
        "category": "Data & Analytics",
        "required_skills": ["Python", "SQL", "Apache Spark", "Snowflake", "dbt", "Airflow", "Data Warehousing"],
        "preferred_skills": ["Kafka", "AWS", "Data Modeling", "Databricks", "CI/CD"],
        "description": "Construct enterprise data mesh architectures, real-time streaming data lakes, and dimensional models powering company-wide machine learning models and executive metrics.",
        "benefits": ["100% Remote", "Unlimited PTO", "Health Savings Account", "Annual Bonus Plan"]
    },
    {
        "id": "JOB-012",
        "title": "Mobile Engineer (React Native / iOS / Android)",
        "company": "PulseApp Mobile",
        "location": "Denver, CO",
        "work_mode": "Hybrid",
        "experience_level": "Mid-Level (3-5 yrs)",
        "min_years_exp": 3,
        "salary_range": "$125,000 - $160,000",
        "min_salary": 125000,
        "category": "Software Development",
        "required_skills": ["React Native", "TypeScript", "JavaScript", "Mobile App Development", "REST APIs", "Git"],
        "preferred_skills": ["Swift", "Kotlin", "Redux", "App Store Deployment", "GraphQL"],
        "description": "Craft smooth 60fps cross-platform mobile experiences with millions of active users. Collaborate closely with product designers and backend engineers to launch high-impact features.",
        "benefits": ["Ski Pass & Wellness Allowance", "Flexible Schedule", "Modern Tech Hardware", "Healthcare Package"]
    },
    {
        "id": "JOB-013",
        "title": "GenAI Solutions Architect",
        "company": "Hyperion Cloud Solutions",
        "location": "San Jose, CA",
        "work_mode": "Hybrid",
        "experience_level": "Lead / Principal (8+ yrs)",
        "min_years_exp": 8,
        "salary_range": "$195,000 - $260,000",
        "min_salary": 195000,
        "category": "AI & Machine Learning",
        "required_skills": ["Python", "Cloud Architecture", "AWS", "LLMs", "Vector Databases", "Enterprise Systems", "Kubernetes"],
        "preferred_skills": ["Azure AI", "GCP Vertex AI", "Consulting Experience", "Security Compliance", "Fine-tuning"],
        "description": "Advise Fortune 500 enterprises on adopting generative AI. Architect secure private cloud RAG foundations, model evaluation frameworks, and cost-effective inference infrastructure.",
        "benefits": ["Tier-1 Stock Options", "Executive Healthcare", "Car & Travel Stipend", "High Bonus Potential"]
    },
    {
        "id": "JOB-014",
        "title": "Site Reliability Engineer (SRE / Observability)",
        "company": "Vortex Network Systems",
        "location": "Remote",
        "work_mode": "Remote",
        "experience_level": "Mid-Level (3-5 yrs)",
        "min_years_exp": 4,
        "salary_range": "$135,000 - $170,000",
        "min_salary": 135000,
        "category": "Cloud & DevOps",
        "required_skills": ["Linux", "Kubernetes", "Prometheus", "Grafana", "Python", "Go", "Incident Management"],
        "preferred_skills": ["OpenTelemetry", "Terraform", "Chaos Engineering", "Datadog", "AWS"],
        "description": "Champion observability, automated recovery, and high availability for global edge network gateways. Transform manual operations into reliable software-driven automation.",
        "benefits": ["Flexible Working Schedule", "Remote Setup Budget", "Continuous Learning Stipend", "401(k) Match"]
    },
    {
        "id": "JOB-015",
        "title": "Frontend Architect (TypeScript & Modern Web)",
        "company": "NextGen Interfaces",
        "location": "Seattle, WA",
        "work_mode": "Remote",
        "experience_level": "Senior (5-8 yrs)",
        "min_years_exp": 6,
        "salary_range": "$150,000 - $195,000",
        "min_salary": 150000,
        "category": "Software Development",
        "required_skills": ["TypeScript", "React", "Next.js", "State Management", "Web Performance", "HTML5", "CSS3"],
        "preferred_skills": ["Tailwind CSS", "Micro-frontends", "Testing (Jest/Playwright)", "WebSockets", "Webpack/Vite"],
        "description": "Own frontend standards, performance budgets, and core architecture for complex browser-based productivity software. Coach engineering squads on scalable UI paradigms.",
        "benefits": ["Annual Technology Allowance", "Unlimited PTO", "Comprehensive Medical", "Home Office Fund"]
    }
]


class JobManager:
    """Manages available job listings with filtering, search, and dynamic additions."""

    def __init__(self, initial_jobs: Optional[List[Dict[str, Any]]] = None):
        self._jobs: List[Dict[str, Any]] = list(initial_jobs or DEFAULT_JOBS)

    def get_all_jobs(self) -> List[Dict[str, Any]]:
        """Return all active job listings."""
        return list(self._jobs)

    def get_job_by_id(self, job_id: str) -> Optional[Dict[str, Any]]:
        """Find a job by its unique ID."""
        for job in self._jobs:
            if job["id"].upper() == job_id.strip().upper():
                return job
        return None

    def add_job(self, job_data: Dict[str, Any]) -> Dict[str, Any]:
        """Add a new job listing to the database."""
        if not job_data.get("id"):
            next_num = len(self._jobs) + 1
            job_data["id"] = f"JOB-{next_num:03d}"
        
        # Ensure list fields
        if isinstance(job_data.get("required_skills"), str):
            job_data["required_skills"] = [s.strip() for s in job_data["required_skills"].split(",") if s.strip()]
        if isinstance(job_data.get("preferred_skills"), str):
            job_data["preferred_skills"] = [s.strip() for s in job_data["preferred_skills"].split(",") if s.strip()]
        if isinstance(job_data.get("benefits"), str):
            job_data["benefits"] = [b.strip() for b in job_data["benefits"].split(",") if b.strip()]

        self._jobs.append(job_data)
        return job_data

    def filter_jobs(
        self,
        category: Optional[str] = None,
        work_mode: Optional[str] = None,
        max_exp: Optional[int] = None,
        min_salary: Optional[int] = None,
        query: Optional[str] = None
    ) -> List[Dict[str, Any]]:
        """Filter jobs based on specified criteria."""
        results = self._jobs

        if category and category != "All":
            results = [j for j in results if j.get("category") == category]

        if work_mode and work_mode != "All":
            results = [j for j in results if j.get("work_mode", "").lower() == work_mode.lower()]

        if max_exp is not None:
            results = [j for j in results if j.get("min_years_exp", 0) <= max_exp]

        if min_salary is not None and min_salary > 0:
            results = [j for j in results if j.get("min_salary", 0) >= min_salary]

        if query and query.strip():
            q = query.strip().lower()
            results = [
                j for j in results
                if q in j["title"].lower()
                or q in j["company"].lower()
                or q in j["description"].lower()
                or any(q in s.lower() for s in j.get("required_skills", []))
            ]

        return results

    def get_categories(self) -> List[str]:
        """Return unique categories."""
        cats = sorted(list({j["category"] for j in self._jobs if "category" in j}))
        return ["All"] + cats


# Singleton instance
job_manager = JobManager()
