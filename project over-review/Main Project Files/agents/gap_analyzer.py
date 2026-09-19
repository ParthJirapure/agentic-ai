"""
Skill Gap Analyzer & 30-Day Career Roadmap Agent
Performs delta analysis between candidate profiles and target roles, calculates
time-to-competency, and creates personalized, actionable week-by-week learning roadmaps.
"""

from typing import Dict, List, Any


# Resource repository mapped to prominent skills
SKILL_RESOURCES = {
    "PyTorch": "Deep Learning with PyTorch (Official Docs & PyTorch Tutorials)",
    "LangChain": "LangChain for LLM Application Development (DeepLearning.AI)",
    "RAG": "Retrieval Augmented Generation: Pinecone Learning Center & LlamaIndex Guides",
    "Vector Databases": "Vector DB Masterclass (Milvus / Pinecone / ChromaDB)",
    "Kubernetes": "Kubernetes Up & Running (Kelsey Hightower) & Certified K8s Administrator (CKA)",
    "Terraform": "HashiCorp Certified Terraform Associate & Learn DevOps Labs",
    "AWS": "AWS Certified Solutions Architect & Hands-on Serverless Workshops",
    "Docker": "Docker for Developers & Container Security Best Practices",
    "FastAPI": "FastAPI Masterclass: Modern High-Performance Python Web APIs",
    "React": "Epic React & The Modern React 19 Handbook",
    "Next.js": "Fullstack Next.js App Router Masterclass & Vercel Academy",
    "TypeScript": "Total TypeScript (Matt Pocock) & Clean Architecture TS",
    "OpenCV": "OpenCV Master Bootcamp: Real-Time Computer Vision & Edge AI",
    "Snowflake": "Snowflake SnowPro Core Certification & Modern Data Engineering",
    "dbt": "dbt Fundamentals & Analytics Engineering Best Practices",
    "Go": "Go: The Complete Developer's Guide (Build Microservices)",
    "Kafka": "Apache Kafka Series: Event Streams & Distributed Real-Time Architecture",
    "Cybersecurity": "CompTIA Security+ / Certified Ethical Hacker (CEH) Labs",
    "Figma": "Figma Design Systems & Advanced Auto-Layout Prototyping"
}

# Project templates based on tech domains
PROJECT_TEMPLATES = {
    "AI & Machine Learning": "Build an Autonomous RAG Research Agent with local Vector Storage, streaming responses, and automated citation verification.",
    "Software Development": "Architect an Event-Driven Microservices API with caching, rate-limiting, Dockerized orchestration, and full CI/CD test automation.",
    "Cloud & DevOps": "Deploy an automated multi-environment Kubernetes cluster using Terraform IaC, ArgoCD GitOps, and Prometheus/Grafana observability.",
    "Data & Analytics": "Design a real-time streaming pipeline ingesting mock transactions with Kafka, transforming via dbt/Spark, and presenting live Grafana dashboards.",
    "Cybersecurity": "Create an automated DevSecOps vulnerability scanner checking Docker containers and Python dependencies in GitHub Actions with Slack alerting.",
    "Product & Design": "Create an end-to-end multi-platform Design System in Figma with design tokens, responsive components, and interactive user validation study."
}


class SkillGapAnalyzerAgent:
    """Agent that identifies candidate skill gaps and designs customized upskilling roadmaps."""

    def analyze_gap(self, candidate_profile: Dict[str, Any], job: Dict[str, Any]) -> Dict[str, Any]:
        """Perform comprehensive gap analysis and generate a personalized 30-day plan."""
        cand_skills = {s.lower(): s for s in candidate_profile.get("skills", [])}
        req_skills = job.get("required_skills", [])
        pref_skills = job.get("preferred_skills", [])

        matched_req = [s for s in req_skills if s.lower() in cand_skills]
        missing_req = [s for s in req_skills if s.lower() not in cand_skills]
        matched_pref = [s for s in pref_skills if s.lower() in cand_skills]
        missing_pref = [s for s in pref_skills if s.lower() not in cand_skills]

        total_missing = len(missing_req) + len(missing_pref)
        estimated_weeks = max(1, min(6, (len(missing_req) * 1.5) + (len(missing_pref) * 0.5)))

        # Identify High-ROI Skill (the missing skill that gives biggest immediate leverage)
        high_roi_skill = missing_req[0] if missing_req else (missing_pref[0] if missing_pref else None)

        category = job.get("category", "Software Development")
        capstone_project = PROJECT_TEMPLATES.get(
            category,
            f"Build a showcase portfolio project implementing {', '.join(missing_req[:2]) if missing_req else 'advanced production patterns'}."
        )

        roadmap = self._generate_30_day_roadmap(missing_req, missing_pref, high_roi_skill, capstone_project)

        return {
            "job_id": job.get("id"),
            "job_title": job.get("title"),
            "company": job.get("company"),
            "matched_required": matched_req,
            "missing_required": missing_req,
            "matched_preferred": matched_pref,
            "missing_preferred": missing_pref,
            "estimated_weeks": round(estimated_weeks, 1),
            "high_roi_skill": high_roi_skill,
            "capstone_project": capstone_project,
            "learning_resources": self._get_resources(missing_req + missing_pref),
            "roadmap": roadmap
        }

    def _get_resources(self, skills: List[str]) -> List[Dict[str, str]]:
        """Match missing skills with curated recommended learning resources."""
        resources = []
        for s in skills:
            for skill_key, res in SKILL_RESOURCES.items():
                if skill_key.lower() in s.lower() or s.lower() in skill_key.lower():
                    resources.append({"skill": s, "resource": res})
                    break
        if not resources and skills:
            for s in skills[:3]:
                resources.append({"skill": s, "resource": f"Official Documentation & GitHub Awesome-{s} Curated Guides"})
        return resources

    def _generate_30_day_roadmap(
        self,
        missing_req: List[str],
        missing_pref: List[str],
        high_roi_skill: str | None,
        capstone_project: str
    ) -> List[Dict[str, Any]]:
        """Construct structured 4-week actionable milestone roadmap."""
        focus_skills = (missing_req + missing_pref)[:4]
        primary = focus_skills[0] if len(focus_skills) > 0 else "Advanced Systems Architecture"
        secondary = focus_skills[1] if len(focus_skills) > 1 else "Performance Optimization"
        tertiary = focus_skills[2] if len(focus_skills) > 2 else "Cloud & Deployment"

        return [
            {
                "week": "Week 1",
                "phase": "Foundational Mastery & Environment Setup",
                "goal": f"Master core syntax, concepts, and mental models of {primary}.",
                "actions": [
                    f"Complete official interactive tutorials and core documentation for {primary}.",
                    "Set up a clean GitHub repository with pre-commit hooks, linting, and automated tests.",
                    f"Build 3 micro-exercises demonstrating fundamental workflows in {primary}."
                ],
                "time_commitment": "6-8 hours"
            },
            {
                "week": "Week 2",
                "phase": "Deep-Dive & Secondary Tooling",
                "goal": f"Integrate {primary} with {secondary} and industry standard patterns.",
                "actions": [
                    f"Explore intermediate & advanced paradigms in {secondary}.",
                    "Implement secure configuration, logging, and error boundaries.",
                    "Review 2 top open-source production repositories using these technologies."
                ],
                "time_commitment": "8-10 hours"
            },
            {
                "week": "Week 3",
                "phase": "High-Impact Capstone Project",
                "goal": "Build and document a tangible portfolio piece that proves competency.",
                "actions": [
                    f"Execute capstone project: '{capstone_project}'",
                    "Write clean README with architecture diagram, installation steps, and live demo link.",
                    "Deploy the project to cloud staging (Vercel, Render, AWS, or Hugging Face Spaces)."
                ],
                "time_commitment": "10-12 hours"
            },
            {
                "week": "Week 4",
                "phase": "Interview Readiness & Resume Integration",
                "goal": "Translate new skills into quantifiable resume accomplishments and ace technical questions.",
                "actions": [
                    f"Update resume with 2 impactful bullet points highlighting your {primary} capstone project.",
                    f"Rehearse top 15 technical interview questions for {primary} and {secondary}.",
                    "Reach out to 3 company insiders or recruiters with a customized project demo."
                ],
                "time_commitment": "5-7 hours"
            }
        ]


# Singleton instance
gap_analyzer = SkillGapAnalyzerAgent()
