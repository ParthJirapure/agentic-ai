"""
Unit tests for AI Job Recommendation Agent modules.
"""

import unittest
from data.jobs_data import JobManager, DEFAULT_JOBS
from agents.resume_analyzer import ResumeAnalyzerAgent
from agents.job_matcher import JobMatcherAgent
from agents.gap_analyzer import SkillGapAnalyzerAgent
from agents.career_copilot import CareerCopilotAgent


class TestJobAgents(unittest.TestCase):

    def setUp(self):
        self.job_manager = JobManager(DEFAULT_JOBS)
        self.resume_analyzer = ResumeAnalyzerAgent()
        self.job_matcher = JobMatcherAgent()
        self.gap_analyzer = SkillGapAnalyzerAgent()
        self.career_copilot = CareerCopilotAgent()

        self.sample_resume = """
        Alex Chen
        Email: alex.chen@example.com | Phone: (555) 123-4567
        LinkedIn: linkedin.com/in/alexchen-dev | GitHub: github.com/alexchen

        Summary:
        Senior Software Engineer with over 5 years of experience architecting AI pipelines and web systems.
        Proficient in Python, PyTorch, LangChain, FastAPI, Docker, and PostgreSQL.
        Education: Master of Science in Computer Science

        Experience:
        AI Engineer | CogniTech (2022 - Present)
        - Developed LLM applications and RAG systems using LangChain, Vector Databases, and PyTorch.
        - Built low-latency REST endpoints with FastAPI and Docker.
        """

    def test_job_manager(self):
        all_jobs = self.job_manager.get_all_jobs()
        self.assertGreaterEqual(len(all_jobs), 15)

        filtered = self.job_manager.filter_jobs(category="AI & Machine Learning")
        self.assertTrue(all(j["category"] == "AI & Machine Learning" for j in filtered))

        new_job = {
            "title": "Test Engineer",
            "company": "QA Systems",
            "location": "Remote",
            "work_mode": "Remote",
            "experience_level": "Mid-Level",
            "min_years_exp": 3,
            "salary_range": "$100k - $120k",
            "min_salary": 100000,
            "category": "Software Development",
            "required_skills": "Python, Selenium, Pytest",
            "preferred_skills": "Docker",
            "description": "Automated testing engineer.",
            "benefits": "Health"
        }
        added = self.job_manager.add_job(new_job)
        self.assertTrue(added["id"].startswith("JOB-"))
        self.assertEqual(len(added["required_skills"]), 3)

    def test_resume_analyzer(self):
        profile = self.resume_analyzer.analyze_resume(
            resume_text=self.sample_resume,
            preferred_role="AI Engineer",
            work_mode_pref="Remote"
        )
        self.assertIn("Python", profile["skills"])
        self.assertIn("PyTorch", profile["skills"])
        self.assertIn("FastAPI", profile["skills"])
        self.assertEqual(profile["years_of_experience"], 5)
        self.assertEqual(profile["education"], "Master's Degree")
        self.assertEqual(profile["contacts"]["email"], "alex.chen@example.com")

    def test_job_matcher(self):
        profile = self.resume_analyzer.analyze_resume(
            resume_text=self.sample_resume,
            preferred_role="AI Engineer",
            work_mode_pref="Remote"
        )
        matches = self.job_matcher.match_jobs(profile, self.job_manager.get_all_jobs())
        self.assertGreater(len(matches), 0)

        top_match = matches[0]
        self.assertIn("overall_score", top_match)
        self.assertIn("agent_explanation", top_match)
        self.assertGreaterEqual(top_match["overall_score"], 60.0)
        self.assertIn("Python", top_match["matched_required_skills"])

    def test_gap_analyzer(self):
        profile = self.resume_analyzer.analyze_resume(resume_text=self.sample_resume)
        job = self.job_manager.get_job_by_id("JOB-001")
        self.assertIsNotNone(job)

        gap_report = self.gap_analyzer.analyze_gap(profile, job)
        self.assertEqual(gap_report["job_id"], "JOB-001")
        self.assertIn("roadmap", gap_report)
        self.assertEqual(len(gap_report["roadmap"]), 4)

    def test_career_copilot(self):
        profile = self.resume_analyzer.analyze_resume(resume_text=self.sample_resume)
        job = self.job_manager.get_job_by_id("JOB-001")

        cover_letter = self.career_copilot.generate_cover_letter(profile, job)
        self.assertIn("CognitiveLabs AI", cover_letter)
        self.assertIn("Python", cover_letter)

        interview_guide = self.career_copilot.generate_interview_prep(profile, job)
        self.assertIn("Technical Deep-Dive", interview_guide)

        critique = self.career_copilot.critique_resume(profile, job)
        self.assertIn("Optimization", critique)


if __name__ == "__main__":
    unittest.main()
