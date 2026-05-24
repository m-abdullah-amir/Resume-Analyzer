"""
prompts.py — All AI prompts for the Resume Analyzer.
Each function returns a fully formatted prompt string ready to send to the LLM.
"""


def get_feedback_prompt(resume_text: str) -> str:
    """Prompt 1 — Detailed resume feedback with strengths and weaknesses."""
    return f"""You are a senior HR specialist and professional resume coach with 10+ years of experience 
reviewing resumes across tech, business, healthcare, and creative industries.

Analyze the following resume thoroughly and provide detailed, actionable feedback.

RESUME TEXT:
\"\"\"
{resume_text}
\"\"\"

INSTRUCTIONS:
1. Evaluate the resume on these criteria:
   - **Formatting & Layout**: Is it clean, scannable, and professional?
   - **Clarity & Conciseness**: Are descriptions clear and impactful?
   - **Achievement-Oriented Language**: Does it use metrics, numbers, and results?
   - **Keyword Optimization**: Does it include industry-relevant keywords?
   - **Section Structure**: Are all essential sections present and well-organized?
   - **Action Verbs**: Does it start bullets with strong action verbs?

2. Provide AT LEAST 5 specific strengths (mark each with ✅)
3. Provide AT LEAST 5 specific weaknesses with concrete improvement suggestions (mark each with ❌)

IMPORTANT RULES:
- Be SPECIFIC, not generic. 
- BAD feedback: "Add more details"
- GOOD feedback: "Your experience bullets lack quantifiable metrics — change 'managed a team' to 'managed a cross-functional team of 8 engineers, delivering 3 projects ahead of schedule'"
- Reference actual content from the resume in your feedback.
- End with a brief overall assessment (2-3 sentences).

Format your response in clean markdown with headers for each section."""


def get_ats_score_prompt(resume_text: str, job_description: str) -> str:
    """Prompt 2 — ATS scoring that returns structured JSON."""
    return f"""You are an advanced ATS (Applicant Tracking System) scoring engine used by Fortune 500 companies.

Score the following resume against the provided job description.

RESUME TEXT:
\"\"\"
{resume_text}
\"\"\"

JOB DESCRIPTION:
\"\"\"
{job_description}
\"\"\"

SCORING CRITERIA:
- **keyword_match** (0-100): How well do the resume keywords match the job description requirements?
- **formatting_score** (0-100): Is the resume formatted in a way that ATS systems can parse correctly?
- **skills_match** (0-100): How many of the required/preferred skills from the JD are present in the resume?
- **experience_relevance** (0-100): How relevant is the candidate's experience to the job requirements?
- **structure_score** (0-100): Does the resume have proper sections (Summary, Skills, Experience, Education)?
- **overall_score** (0-100): Weighted average considering all factors above.

Respond ONLY with valid JSON. No explanation. No markdown. No backticks. No extra text.

Example format:
{{"overall_score": 78, "keyword_match": 80, "formatting_score": 70, "skills_match": 85, "experience_relevance": 75, "structure_score": 80}}"""


def get_missing_skills_prompt(resume_text: str, job_description: str) -> str:
    """Prompt 3 — Identify found and missing skills."""
    return f"""You are an expert technical recruiter. Analyze the resume against the job description 
and identify which required skills are present and which are missing.

RESUME TEXT:
\"\"\"
{resume_text}
\"\"\"

JOB DESCRIPTION:
\"\"\"
{job_description}
\"\"\"

INSTRUCTIONS:
1. Extract ALL required and preferred skills/technologies/qualifications from the job description.
2. Check each skill against the resume content.
3. Categorize every skill as either "found" or "missing".
4. Be thorough — check for synonyms and related terms (e.g., "ML" = "Machine Learning").

Respond ONLY with valid JSON. No explanation. No markdown. No backticks. No extra text.

Example format:
{{"found": ["Python", "SQL", "Machine Learning"], "missing": ["Docker", "Kubernetes", "TensorFlow"]}}"""


def get_restructure_prompt(resume_text: str, job_description: str) -> str:
    """Prompt 4 — Rewrite the resume as structured JSON for template rendering."""
    return f"""You are an elite executive resume writer with expertise in ATS optimization.

Rewrite the following resume in a highly professional, formal, and ATS-optimized format.

ORIGINAL RESUME:
\"\"\"
{resume_text}
\"\"\"

TARGET JOB DESCRIPTION:
\"\"\"
{job_description}
\"\"\"

STRICT RULES:
1. Improve the structure, phrasing, formatting, and impact to make it highly professional.
2. Carefully weave in relevant keywords from the JOB DESCRIPTION naturally.
3. You may rephrase bullets to better highlight relevant skills, but do NOT invent fake jobs or degrees.
4. For experience bullets: start each with a strong action verb (Led, Engineered, Spearheaded, Architected, Optimized). Add quantifiable metrics or placeholders like [X]%.
5. Write a powerful 3-4 sentence professional summary tailored to the job description.
6. Categorize skills into logical groups (e.g., "Programming Languages", "Frameworks", etc.).

Respond ONLY with valid JSON. No explanation. No markdown. No backticks. No extra text.

EXACT FORMAT:
{{
    "name": "Candidate Full Name",
    "contact": {{
        "email": "email@example.com",
        "phone": "+1 234 567 8900",
        "location": "City, Country",
        "linkedin": "linkedin.com/in/username"
    }},
    "summary": "Professional summary text here...",
    "skills": {{
        "Programming Languages": ["Python", "Java", "C++"],
        "Frameworks & Tools": ["React", "Node.js"],
        "Databases": ["PostgreSQL", "MongoDB"]
    }},
    "experience": [
        {{
            "title": "Job Title",
            "company": "Company Name",
            "duration": "Jan 2023 – Present",
            "bullets": [
                "Led a team of 8 engineers to deliver...",
                "Engineered a scalable microservices architecture..."
            ]
        }}
    ],
    "education": [
        {{
            "degree": "Bachelor of Science in Computer Science",
            "institution": "University Name",
            "year": "Expected 2028",
            "details": "Relevant coursework or honors"
        }}
    ],
    "projects": [
        {{
            "name": "Project Name",
            "description": "Built a full-stack application that improved X by Y%"
        }}
    ],
    "certifications": ["AWS Cloud Practitioner", "Google Data Analytics"]
}}"""


def get_cover_letter_prompt(resume_text: str, job_description: str) -> str:
    """Prompt 5 — Generate a cover letter as structured JSON for template rendering."""
    return f"""You are a professional career coach and cover letter specialist. Write a compelling, 
personalized cover letter based on the candidate's resume and the target job description.

RESUME TEXT:
\"\"\"
{resume_text}
\"\"\"

JOB DESCRIPTION:
\"\"\"
{job_description}
\"\"\"

INSTRUCTIONS:
1. Opening paragraph: Express enthusiasm for the specific role. Mention how you found the role.
2. Body paragraph 1: Highlight 2-3 most relevant experiences that directly match the job requirements. Use specific metrics.
3. Body paragraph 2: Demonstrate knowledge of the company/industry and explain why you're a cultural fit.
4. Closing paragraph: Restate interest, mention availability for an interview.

STRICT RULES:
- Keep it to 250-350 words total across all paragraphs.
- Use a professional but warm tone — not robotic.
- Reference ACTUAL skills and experiences from the resume — do NOT invent anything.
- Tailor EVERY sentence to the specific job description.

Respond ONLY with valid JSON. No explanation. No markdown. No backticks. No extra text.

EXACT FORMAT:
{{
    "sender_name": "Candidate Full Name",
    "sender_contact": "email@example.com | +1 234 567 8900 | City, Country",
    "date": "May 24, 2026",
    "recipient": "Hiring Manager",
    "company": "Company Name from JD",
    "subject": "Application for [Job Title] Position",
    "paragraphs": [
        "Opening paragraph expressing enthusiasm for the role...",
        "Body paragraph highlighting relevant experience and achievements...",
        "Body paragraph about cultural fit and company knowledge...",
        "Closing paragraph restating interest and availability..."
    ],
    "sign_off": "Sincerely"
}}"""


def get_interview_questions_prompt(resume_text: str, job_description: str) -> str:
    """Prompt 6 — Generate likely interview questions based on resume and job description."""
    return f"""You are a senior technical interviewer and hiring manager with 15 years of experience 
conducting interviews at top companies.

Based on the candidate's resume and the job description, generate interview questions they are 
likely to face.

RESUME TEXT:
\"\"\"
{resume_text}
\"\"\"

JOB DESCRIPTION:
\"\"\"
{job_description}
\"\"\"

Generate questions in these categories:

**🎯 Role-Specific Technical Questions (5 questions)**
- Questions based on the skills and technologies mentioned in the job description
- Include expected answer hints for each question

**💼 Behavioral Questions (5 questions)**
- STAR-method questions based on the candidate's experience
- Reference specific projects or roles from their resume

**🔍 Resume Deep-Dive Questions (3 questions)**
- Questions an interviewer would ask about gaps, transitions, or interesting points in the resume

**⚡ Curveball Questions (2 questions)**
- Unexpected but relevant questions that test problem-solving

For each question, provide:
1. The question itself
2. A brief "💡 How to answer" tip (2-3 sentences)

Format your response in clean markdown with headers for each category."""


def get_skill_recommendations_prompt(resume_text: str, job_description: str) -> str:
    """Prompt 7 — Suggest courses, certifications, and learning paths for missing skills."""
    return f"""You are a career development advisor and learning path specialist who helps professionals 
upskill efficiently.

Based on the candidate's current skills (from their resume) and the target role requirements 
(from the job description), recommend specific courses and certifications.

RESUME TEXT:
\"\"\"
{resume_text}
\"\"\"

JOB DESCRIPTION:
\"\"\"
{job_description}
\"\"\"

Provide recommendations in this EXACT JSON format. Respond ONLY with valid JSON. No explanation. No markdown. No backticks.

{{
    "priority_skills": [
        {{
            "skill": "Skill Name",
            "importance": "Critical/High/Medium",
            "free_courses": [
                {{"name": "Course Name", "platform": "Platform", "url": "URL", "duration": "X hours"}},
                {{"name": "Course Name", "platform": "Platform", "url": "URL", "duration": "X hours"}}
            ],
            "certifications": [
                {{"name": "Cert Name", "provider": "Provider", "cost": "Free/$X", "url": "URL"}}
            ]
        }}
    ],
    "learning_path": "A 2-3 sentence recommended learning order/strategy"
}}

RULES:
- Recommend ONLY real, existing courses and certifications with accurate URLs.
- Prioritize FREE resources (Coursera audit, freeCodeCamp, Khan Academy, YouTube, MIT OCW, Google certs).
- Include 3-5 priority skills maximum.
- Focus on skills that are MISSING or WEAK in the resume but REQUIRED in the job description."""


def get_multi_resume_comparison_prompt(resumes: dict, job_description: str) -> str:
    """Prompt 8 — Compare multiple resumes and rank them against the job description."""
    resumes_text = ""
    for filename, text in resumes.items():
        resumes_text += f"\n--- RESUME: {filename} ---\n{text}\n"

    return f"""You are an expert HR recruiter and ATS system. Your task is to evaluate and rank multiple 
candidates against a specific job description.

JOB DESCRIPTION:
\"\"\"
{job_description}
\"\"\"

CANDIDATE RESUMES:
{resumes_text}

INSTRUCTIONS:
1. Analyze each candidate's resume against the core requirements of the job description.
2. Calculate a score (0-100) for each candidate based on skills, experience relevance, and overall fit.
3. Determine the final ranking of the candidates (from best fit to worst fit).
4. Provide a brief (1-2 sentence) justification for each candidate's ranking.

Respond ONLY with valid JSON in this exact format. No markdown, no backticks, no explanations.

{{
    "rankings": [
        {{
            "rank": 1,
            "filename": "candidate1.pdf",
            "score": 92,
            "justification": "Strongest match with required Python and SQL skills, plus relevant industry experience."
        }},
        {{
            "rank": 2,
            "filename": "candidate2.docx",
            "score": 85,
            "justification": "Good technical skills, but lacks the required machine learning experience."
        }}
    ]
}}"""

