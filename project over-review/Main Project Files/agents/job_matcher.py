"""
Job Matcher Agent
Implements a multi-factor hybrid matching engine that scores candidates against
job listings using Jaccard skill overlap, TF-IDF semantic embeddings, experience curve
weighting, and preference alignment.
"""

from typing import List, Dict, Any, Optional
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


class JobMatcherAgent:
    """Intelligent recommendation engine that pairs candidates with optimal opportunities."""

    def __init__(self):
        self.vectorizer = TfidfVectorizer(stop_words="english")

    def _calculate_skill_score(
        self,
        candidate_skills: List[str],
        required_skills: List[str],
        preferred_skills: List[str],
        job_description: str
    ) -> Dict[str, Any]:
        """Compute exact match ratio, missing skills, and semantic similarity."""
        cand_set = {s.lower() for s in candidate_skills}
        req_set = {s.lower() for s in required_skills}
        pref_set = {s.lower() for s in preferred_skills}

        matched_req = [s for s in required_skills if s.lower() in cand_set]
        missing_req = [s for s in required_skills if s.lower() not in cand_set]

        matched_pref = [s for s in preferred_skills if s.lower() in cand_set]
        missing_pref = [s for s in preferred_skills if s.lower() not in cand_set]

        # Jaccard / Overlap Ratio on Required Skills
        req_ratio = len(matched_req) / len(required_skills) if required_skills else 1.0

        # Preferred Bonus
        pref_bonus = (len(matched_pref) / len(preferred_skills) * 0.15) if preferred_skills else 0.0

        # TF-IDF Semantic Similarity
        cand_corpus = " ".join(candidate_skills) if candidate_skills else "general developer"
        job_corpus = f"{' '.join(required_skills)} {' '.join(preferred_skills)} {job_description}"

        try:
            tfidf_matrix = self.vectorizer.fit_transform([cand_corpus, job_corpus])
            semantic_sim = float(cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:2])[0][0])
        except Exception:
            semantic_sim = req_ratio

        # Weighted Skill Score (0 - 100)
        skill_score = min(100.0, ((req_ratio * 0.70) + (semantic_sim * 0.20) + pref_bonus) * 100.0)

        return {
            "skill_score": round(skill_score, 1),
            "matched_req": matched_req,
            "missing_req": missing_req,
            "matched_pref": matched_pref,
            "missing_pref": missing_pref,
            "semantic_similarity": round(semantic_sim * 100, 1)
        }

    def _calculate_experience_score(self, candidate_exp: int, min_required_exp: int) -> float:
        """Evaluate candidate experience against job requirements."""
        if min_required_exp <= 0:
            return 100.0

        if candidate_exp >= min_required_exp:
            # Full score, slight bonus for solid seniority without overqualification penalty
            diff = candidate_exp - min_required_exp
            if diff <= 4:
                return 100.0
            else:
                return 95.0  # Slight taper for overqualification
        else:
            # Underqualified curve: give partial credit
            ratio = candidate_exp / min_required_exp
            return max(30.0, round(ratio * 85.0, 1))

    def _calculate_preference_score(
        self,
        job: Dict[str, Any],
        preferred_role: Optional[str],
        work_mode_pref: str,
        min_salary_pref: int
    ) -> float:
        """Score alignment with user preferences."""
        score = 100.0
        penalties = 0.0

        # Work Mode
        job_mode = job.get("work_mode", "").lower()
        pref_mode = (work_mode_pref or "Any").lower()
        if pref_mode != "any" and pref_mode != job_mode:
            penalties += 20.0

        # Salary
        job_min_salary = job.get("min_salary", 0)
        if min_salary_pref > 0 and job_min_salary > 0:
            if job_min_salary < min_salary_pref:
                gap_pct = (min_salary_pref - job_min_salary) / min_salary_pref
                penalties += min(25.0, gap_pct * 40.0)

        # Role alignment
        if preferred_role and preferred_role.strip():
            target = preferred_role.strip().lower()
            job_title = job.get("title", "").lower()
            category = job.get("category", "").lower()
            if any(word in job_title or word in category for word in target.split() if len(word) > 2):
                score += 5.0
            else:
                penalties += 10.0

        final_score = max(35.0, min(100.0, score - penalties))
        return round(final_score, 1)

    def _generate_explanation(
        self,
        job: Dict[str, Any],
        overall_score: float,
        skill_res: Dict[str, Any],
        candidate_exp: int
    ) -> str:
        """Generate conversational AI recruiter justification for the match."""
        title = job.get("title", "Position")
        company = job.get("company", "the company")
        min_exp = job.get("min_years_exp", 0)
        matched_req = skill_res["matched_req"]
        missing_req = skill_res["missing_req"]

        bullets = []

        if len(matched_req) >= 4:
            bullets.append(f"⭐ **Exceptional Core Synergy**: You possess {len(matched_req)} essential technologies ({', '.join(matched_req[:4])}).")
        elif len(matched_req) > 0:
            bullets.append(f"✅ **Core Skill Match**: Matched on {len(matched_req)} required skills: {', '.join(matched_req)}.")
        else:
            bullets.append("⚠️ **Skill Pivot**: This role represents a directional pivot; foundational tech crossover detected.")

        if candidate_exp >= min_exp:
            bullets.append(f"💼 **Experience Fit**: Your ~{candidate_exp} years meets or exceeds the required {min_exp}+ years.")
        else:
            bullets.append(f"📈 **Stretch Opportunity**: Job asks for {min_exp}+ yrs vs your ~{candidate_exp} yrs, making it a high-growth career step.")

        if missing_req:
            bullets.append(f"🎯 **Bridgeable Gaps**: Upskilling in `{', '.join(missing_req[:3])}` will position you as a prime candidate.")
        else:
            bullets.append("🌟 **Ready to Apply**: 100% of core required capabilities verified in your profile.")

        summary_intro = f"**{title}** at **{company}** earns a **{overall_score:.0f}% Match Rating**."
        return f"{summary_intro}\n\n" + "\n".join(f"- {b}" for b in bullets)

    def match_jobs(
        self,
        candidate_profile: Dict[str, Any],
        jobs: List[Dict[str, Any]],
        min_match_threshold: float = 40.0,
        category_filter: str = "All",
        work_mode_filter: str = "All"
    ) -> List[Dict[str, Any]]:
        """Score, rank, and annotate all candidate opportunities."""
        cand_skills = candidate_profile.get("skills", [])
        cand_exp = candidate_profile.get("years_of_experience", 2)
        pref_role = candidate_profile.get("preferred_role", "")
        pref_mode = candidate_profile.get("work_mode_preference", "Any")
        pref_salary = candidate_profile.get("min_salary_preference", 0)

        results = []

        for job in jobs:
            # Apply UI category / work mode filter
            if category_filter and category_filter != "All" and job.get("category") != category_filter:
                continue
            if work_mode_filter and work_mode_filter != "All" and job.get("work_mode", "").lower() != work_mode_filter.lower():
                continue

            # Skill Scoring
            skill_res = self._calculate_skill_score(
                cand_skills,
                job.get("required_skills", []),
                job.get("preferred_skills", []),
                job.get("description", "")
            )

            # Experience Scoring
            exp_score = self._calculate_experience_score(cand_exp, job.get("min_years_exp", 0))

            # Preference Alignment
            pref_score = self._calculate_preference_score(job, pref_role, pref_mode, pref_salary)

            # Composite Overall Match Score
            overall_score = round((skill_res["skill_score"] * 0.50) + (exp_score * 0.25) + (pref_score * 0.25), 1)

            if overall_score < min_match_threshold:
                continue

            # Match Tier
            if overall_score >= 88:
                tier = "🌟 Top Match"
                badge_color = "emerald"
            elif overall_score >= 75:
                tier = "✅ Strong Fit"
                badge_color = "blue"
            elif overall_score >= 60:
                tier = "⚡ Moderate Fit"
                badge_color = "amber"
            else:
                tier = "🌱 Stretch Goal"
                badge_color = "purple"

            explanation = self._generate_explanation(job, overall_score, skill_res, cand_exp)

            job_match = dict(job)
            job_match.update({
                "overall_score": overall_score,
                "skill_score": skill_res["skill_score"],
                "exp_score": exp_score,
                "pref_score": pref_score,
                "semantic_similarity": skill_res["semantic_similarity"],
                "matched_required_skills": skill_res["matched_req"],
                "missing_required_skills": skill_res["missing_req"],
                "matched_preferred_skills": skill_res["matched_pref"],
                "missing_preferred_skills": skill_res["missing_pref"],
                "match_tier": tier,
                "badge_color": badge_color,
                "agent_explanation": explanation
            })
            results.append(job_match)

        # Sort by overall match descending
        results.sort(key=lambda x: x["overall_score"], reverse=True)
        return results


# Singleton instance
job_matcher = JobMatcherAgent()
