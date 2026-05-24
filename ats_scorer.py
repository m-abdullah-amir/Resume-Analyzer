"""
ats_scorer.py — Hybrid ATS scoring: rule-based checks + AI analysis.
Combines deterministic checks with LLM evaluation for reliable scoring.
"""

import re
from llm_analyzer import analyze_json
from prompts import get_ats_score_prompt


def calculate_rule_based_score(resume_text: str) -> dict:
    """
    Pure Python rule-based ATS checks. No AI needed.
    Returns a dict with individual check results and total score (out of 75).
    """
    text_lower = resume_text.lower()
    words = resume_text.split()
    word_count = len(words)

    checks = {}

    # 1. Has a Skills section? (+10)
    skills_keywords = ["skills", "technical skills", "core competencies", "technologies", "proficiencies"]
    checks["skills_section"] = {
        "label": "Skills Section Found",
        "passed": any(kw in text_lower for kw in skills_keywords),
        "points": 10,
    }

    # 2. Has Experience / Work History section? (+10)
    exp_keywords = ["experience", "work history", "employment", "professional experience", "work experience"]
    checks["experience_section"] = {
        "label": "Experience Section Found",
        "passed": any(kw in text_lower for kw in exp_keywords),
        "points": 10,
    }

    # 3. Has Education section? (+10)
    edu_keywords = ["education", "academic", "degree", "university", "bachelor", "master", "phd"]
    checks["education_section"] = {
        "label": "Education Section Found",
        "passed": any(kw in text_lower for kw in edu_keywords),
        "points": 10,
    }

    # 4. Has contact info — email and phone? (+10)
    has_email = bool(re.search(r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}", resume_text))
    has_phone = bool(re.search(r"[\+]?[\d\s\-\(\)]{7,15}", resume_text))
    checks["contact_info"] = {
        "label": "Contact Information (Email/Phone)",
        "passed": has_email and has_phone,
        "points": 10,
    }

    # 5. Contains quantifiable metrics? (+15)
    has_metrics = bool(re.search(r"\d+[%+]|\$[\d,]+|\d+\s*(years?|months?|projects?|clients?|team|members?)", text_lower))
    checks["metrics"] = {
        "label": "Quantifiable Metrics & Numbers",
        "passed": has_metrics,
        "points": 15,
    }

    # 6. Ideal word count 300-800? (+10)
    checks["word_count"] = {
        "label": f"Word Count ({word_count} words — ideal: 300–800)",
        "passed": 300 <= word_count <= 800,
        "points": 10,
    }

    # 7. Has Summary/Objective section? (+10)
    summary_keywords = ["summary", "objective", "profile", "about me", "professional summary"]
    checks["summary_section"] = {
        "label": "Summary / Objective Section",
        "passed": any(kw in text_lower for kw in summary_keywords),
        "points": 10,
    }

    # Calculate total
    total = sum(c["points"] for c in checks.values() if c["passed"])

    return {"checks": checks, "rule_score": total, "max_score": 75}


def get_ai_score(resume_text: str, job_description: str) -> dict | None:
    """
    Get AI-based ATS score from Groq via structured JSON response.
    Returns the parsed score dict or None on failure.
    """
    prompt = get_ats_score_prompt(resume_text, job_description)
    return analyze_json(prompt)


def calculate_final_score(resume_text: str, job_description: str) -> dict:
    """
    Hybrid scoring: rule-based (75 points) + AI score (25 points) = 100 total.
    
    Returns a comprehensive scoring result dict.
    """
    # Rule-based scoring
    rule_result = calculate_rule_based_score(resume_text)
    rule_score = rule_result["rule_score"]  # out of 75

    # AI-based scoring
    ai_raw = get_ai_score(resume_text, job_description)

    if ai_raw and "overall_score" in ai_raw:
        # Normalize AI score to be out of 25
        ai_score_normalized = round(ai_raw["overall_score"] * 25 / 100)
        ai_breakdown = {
            "keyword_match": ai_raw.get("keyword_match", 0),
            "formatting_score": ai_raw.get("formatting_score", 0),
            "skills_match": ai_raw.get("skills_match", 0),
            "experience_relevance": ai_raw.get("experience_relevance", 0),
            "structure_score": ai_raw.get("structure_score", 0),
        }
    else:
        # Fallback if AI fails — give a neutral midpoint
        ai_score_normalized = 13
        ai_breakdown = {
            "keyword_match": "N/A",
            "formatting_score": "N/A",
            "skills_match": "N/A",
            "experience_relevance": "N/A",
            "structure_score": "N/A",
        }

    final_score = rule_score + ai_score_normalized

    return {
        "final_score": min(final_score, 100),
        "rule_score": rule_score,
        "rule_max": 75,
        "ai_score_normalized": ai_score_normalized,
        "ai_max": 25,
        "ai_breakdown": ai_breakdown,
        "rule_checks": rule_result["checks"],
    }
