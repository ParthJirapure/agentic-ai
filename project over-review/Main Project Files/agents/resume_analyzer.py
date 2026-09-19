"""
Resume Analyzer Agent
Extracts text from PDF/TXT resumes, identifies technical and soft skills,
infers experience duration, education, and builds a structured candidate profile.
"""

import re
import os
from typing import Dict, List, Any, Optional

try:
    from pypdf import PdfReader
except ImportError:
    PdfReader = None


# Comprehensive Master Skills Taxonomy
SKILL_TAXONOMY = {
    "Programming Languages": [
        "Python", "JavaScript", "TypeScript", "Go", "Golang", "C++", "C#", "Java",
        "Rust", "Swift", "Kotlin", "SQL", "Bash", "Shell", "PHP", "Ruby", "R", "Scala", "C"
    ],
    "Frameworks & Libraries": [
        "React", "Next.js", "Node.js", "FastAPI", "Flask", "Django", "PyTorch",
        "TensorFlow", "Scikit-Learn", "Pandas", "NumPy", "OpenCV", "LangChain",
        "LlamaIndex", "Keras", "Vue", "Angular", "Express", "Tailwind CSS",
        "Redux", "GraphQL", "Hugging Face", "vLLM", "Selenium", "Spring Boot"
    ],
    "Cloud & Infrastructure": [
        "AWS", "Azure", "GCP", "Google Cloud", "Docker", "Kubernetes", "Terraform",
        "CI/CD", "Linux", "Helm", "Prometheus", "Grafana", "ArgoCD", "Ansible",
        "Jenkins", "Git", "GitHub Actions", "Kafka", "Redis", "Nginx"
    ],
    "Data & AI": [
        "Machine Learning", "Deep Learning", "LLMs", "Generative AI", "RAG",
        "Vector Databases", "Data Warehousing", "Snowflake", "Databricks",
        "Apache Spark", "Airflow", "dbt", "Tableau", "Power BI", "A/B Testing",
        "Data Modeling", "Computer Vision", "Natural Language Processing", "NLP"
    ],
    "Databases & Storage": [
        "PostgreSQL", "MySQL", "MongoDB", "Redis", "Cassandra", "DynamoDB",
        "Elasticsearch", "Pinecone", "ChromaDB", "Milvus", "Qdrant", "SQLite"
    ],
    "Product, Design & Methodologies": [
        "Figma", "UI Design", "UX Research", "Design Systems", "Prototyping",
        "Wireframing", "Product Management", "Agile", "Scrum", "Roadmapping",
        "User Research", "System Architecture", "Microservices", "REST APIs", "gRPC"
    ],
    "Cybersecurity": [
        "Cybersecurity", "Network Security", "Penetration Testing", "SIEM",
        "Cloud Security", "Incident Response", "Vulnerability Management", "CISSP"
    ]
}

ALL_KNOWN_SKILLS = []
for cat_skills in SKILL_TAXONOMY.values():
    ALL_KNOWN_SKILLS.extend(cat_skills)
ALL_KNOWN_SKILLS = list(dict.fromkeys(ALL_KNOWN_SKILLS))  # Deduplicate while preserving order


class ResumeAnalyzerAgent:
    """Autonomous agent that parses resumes and constructs structured candidate profiles."""

    def __init__(self):
        self.skills_lookup = {skill.lower(): skill for skill in ALL_KNOWN_SKILLS}

    def extract_text_from_file(self, file_path: str) -> str:
        """Extract text content from uploaded file (PDF or TXT)."""
        if not file_path or not os.path.exists(file_path):
            return ""

        ext = os.path.splitext(file_path)[1].lower()

        if ext == ".pdf":
            if PdfReader is None:
                return "Error: pypdf library is not installed."
            try:
                reader = PdfReader(file_path)
                text = ""
                for page in reader.pages:
                    page_text = page.extract_text()
                    if page_text:
                        text += page_text + "\n"
                return text.strip()
            except Exception as e:
                return f"Error reading PDF: {str(e)}"

        elif ext in [".txt", ".md"]:
            try:
                with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
                    return f.read().strip()
            except Exception as e:
                return f"Error reading text file: {str(e)}"

        return "Unsupported file format. Please upload a PDF or TXT resume."

    def extract_skills(self, text: str, additional_skills: Optional[str] = None) -> List[str]:
        """Extract recognized skills from text using boundary-aware pattern matching."""
        found_skills = set()
        text_lower = f" {text.lower()} "

        for skill_lower, original_name in self.skills_lookup.items():
            # Build regex with word boundaries (allowing special characters like C++, C#, .js)
            escaped = re.escape(skill_lower)
            pattern = rf"(?:\b|(?<=[^a-zA-Z0-9]))" + escaped + rf"(?:\b|(?=[^a-zA-Z0-9]))"
            if re.search(pattern, text_lower):
                found_skills.add(original_name)

        # Handle user-provided additional skills
        if additional_skills:
            for s in additional_skills.split(","):
                clean = s.strip()
                if clean:
                    found_skills.add(clean)

        return sorted(list(found_skills), key=lambda x: x.lower())

    def extract_experience_years(self, text: str, manual_override: Optional[int] = None) -> int:
        """Detect total years of professional experience from resume text."""
        if manual_override is not None and manual_override > 0:
            return manual_override

        # Regex patterns for experience
        patterns = [
            r"(\d+)\+?\s*(?:years|yrs)\s+(?:of\s+)?experience",
            r"experience\s*:\s*(\d+)\+?\s*(?:years|yrs)",
            r"over\s+(\d+)\s+years",
            r"(\d+)\+?\s+years\s+in\s+software",
            r"(\d+)\+?\s+years\s+as\s+a"
        ]

        found_years = []
        for pattern in patterns:
            matches = re.findall(pattern, text, re.IGNORECASE)
            for m in matches:
                try:
                    val = int(m)
                    if 1 <= val <= 35:
                        found_years.append(val)
                except ValueError:
                    continue

        if found_years:
            return max(found_years)

        # Fallback heuristic: look for year spans (e.g., 2019-2024)
        year_ranges = re.findall(r"(20\d\d)\s*[-–—to]+\s*(20\d\d|present|current)", text, re.IGNORECASE)
        if year_ranges:
            total_span = 0
            for start_y, end_y in year_ranges:
                try:
                    s = int(start_y)
                    e = 2026 if any(k in end_y.lower() for k in ["present", "current"]) else int(end_y)
                    if 2000 <= s <= e <= 2026:
                        total_span = max(total_span, e - s)
                except ValueError:
                    pass
            if total_span > 0:
                return min(total_span, 25)

        return 2  # Default conservative assumption

    def extract_contact_info(self, text: str) -> Dict[str, str]:
        """Extract email, phone, and professional links."""
        contact = {"email": "", "phone": "", "linkedin": "", "github": ""}

        # Email
        email_match = re.search(r"[\w\.-]+@[\w\.-]+\.\w+", text)
        if email_match:
            contact["email"] = email_match.group(0)

        # Phone
        phone_match = re.search(r"(?:\+?\d{1,3}[-.\s]?)?\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}", text)
        if phone_match:
            contact["phone"] = phone_match.group(0).strip()

        # LinkedIn
        li_match = re.search(r"(?:linkedin\.com/in/)([\w-]+)", text, re.IGNORECASE)
        if li_match:
            contact["linkedin"] = f"https://linkedin.com/in/{li_match.group(1)}"

        # GitHub
        gh_match = re.search(r"(?:github\.com/)([\w-]+)", text, re.IGNORECASE)
        if gh_match:
            contact["github"] = f"https://github.com/{gh_match.group(1)}"

        return contact

    def extract_education(self, text: str) -> str:
        """Infer highest education level from resume text."""
        text_lower = text.lower()
        if any(deg in text_lower for deg in ["ph.d", "phd", "doctor of philosophy"]):
            return "Ph.D. / Doctorate"
        elif any(deg in text_lower for deg in ["master", "m.s.", "m.tech", "mba", "msc"]):
            return "Master's Degree"
        elif any(deg in text_lower for deg in ["bachelor", "b.s.", "b.tech", "bsc", "b.e."]):
            return "Bachelor's Degree"
        elif "associate" in text_lower:
            return "Associate Degree"
        return "Self-Taught / Professional Experience"

    def analyze_resume(
        self,
        resume_text: str,
        file_path: Optional[str] = None,
        manual_skills: Optional[str] = None,
        manual_exp: Optional[int] = None,
        preferred_role: Optional[str] = None,
        work_mode_pref: str = "Any",
        min_salary_pref: int = 0
    ) -> Dict[str, Any]:
        """Comprehensive analysis producing a structured Candidate Profile."""
        combined_text = resume_text

        if file_path and os.path.exists(file_path):
            extracted = self.extract_text_from_file(file_path)
            if extracted and not extracted.startswith("Error"):
                combined_text = f"{extracted}\n\n{combined_text}"

        skills = self.extract_skills(combined_text, manual_skills)
        exp_years = self.extract_experience_years(combined_text, manual_exp)
        contacts = self.extract_contact_info(combined_text)
        education = self.extract_education(combined_text)

        # Categorize detected skills
        categorized_skills: Dict[str, List[str]] = {}
        for cat, cat_list in SKILL_TAXONOMY.items():
            matches = [s for s in skills if s in cat_list]
            if matches:
                categorized_skills[cat] = matches

        profile = {
            "skills": skills,
            "skills_count": len(skills),
            "categorized_skills": categorized_skills,
            "years_of_experience": exp_years,
            "education": education,
            "contacts": contacts,
            "raw_text_length": len(combined_text),
            "preferred_role": preferred_role.strip() if preferred_role else "Software & AI Roles",
            "work_mode_preference": work_mode_pref,
            "min_salary_preference": min_salary_pref,
            "preview_summary": f"Detected {len(skills)} verified skills across {len(categorized_skills)} domains with ~{exp_years} years of professional experience."
        }

        return profile


# Singleton instance
resume_analyzer = ResumeAnalyzerAgent()
