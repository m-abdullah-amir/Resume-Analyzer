"""
html_templates.py — Professional HTML/CSS templates for resume and cover letter rendering.
The AI outputs structured JSON; these templates guarantee a perfect, consistent design.
"""


def render_resume_html(data: dict) -> str:
    """
    Render a professional resume from structured data.
    
    Expected data format:
    {
        "name": "John Doe",
        "contact": {"email": "...", "phone": "...", "location": "...", "linkedin": "..."},
        "summary": "Professional summary text...",
        "skills": {"Category Name": ["Skill1", "Skill2"], ...},
        "experience": [
            {
                "title": "Job Title",
                "company": "Company Name",
                "duration": "Jan 2023 – Present",
                "bullets": ["Achievement 1", "Achievement 2"]
            }
        ],
        "education": [
            {
                "degree": "BS in Computer Science",
                "institution": "University Name",
                "year": "2024",
                "details": "Optional details"
            }
        ],
        "projects": [
            {"name": "Project Name", "description": "What you did and the result"}
        ],
        "certifications": ["Cert 1", "Cert 2"]
    }
    """
    name = data.get("name", "Your Name")
    contact = data.get("contact", {})
    summary = data.get("summary", "")
    skills = data.get("skills", {})
    experience = data.get("experience", [])
    education = data.get("education", [])
    projects = data.get("projects", [])
    certifications = data.get("certifications", [])

    # Build contact line
    contact_parts = []
    if contact.get("email"):
        contact_parts.append(f'<span>{contact["email"]}</span>')
    if contact.get("phone"):
        contact_parts.append(f'<span>{contact["phone"]}</span>')
    if contact.get("location"):
        contact_parts.append(f'<span>{contact["location"]}</span>')
    if contact.get("linkedin"):
        contact_parts.append(f'<span>{contact["linkedin"]}</span>')
    contact_html = ' <span class="separator">|</span> '.join(contact_parts)

    # Build skills section
    skills_html = ""
    for category, skill_list in skills.items():
        pills = "".join([f'<span class="skill-pill">{s}</span>' for s in skill_list])
        skills_html += f'<div class="skill-category"><span class="skill-cat-label">{category}:</span> {pills}</div>'

    # Build experience section
    exp_html = ""
    for job in experience:
        bullets = "".join([f"<li>{b}</li>" for b in job.get("bullets", [])])
        exp_html += f"""
        <div class="job">
            <div class="job-header">
                <div class="job-left">
                    <div class="job-title">{job.get('title', '')}</div>
                    <div class="job-company">{job.get('company', '')}</div>
                </div>
                <div class="job-duration">{job.get('duration', '')}</div>
            </div>
            <ul class="job-bullets">{bullets}</ul>
        </div>"""

    # Build education section
    edu_html = ""
    for edu in education:
        details = f'<div class="edu-details">{edu.get("details", "")}</div>' if edu.get("details") else ""
        edu_html += f"""
        <div class="edu-item">
            <div class="job-header">
                <div class="job-left">
                    <div class="job-title">{edu.get('degree', '')}</div>
                    <div class="job-company">{edu.get('institution', '')}</div>
                </div>
                <div class="job-duration">{edu.get('year', '')}</div>
            </div>
            {details}
        </div>"""

    # Build projects section
    proj_html = ""
    if projects:
        for proj in projects:
            proj_html += f"""
            <div class="project-item">
                <span class="project-name">{proj.get('name', '')}</span>
                <span class="project-desc"> — {proj.get('description', '')}</span>
            </div>"""

    # Build certifications section
    cert_html = ""
    if certifications and certifications != ["None"] and certifications != [""]:
        cert_items = "".join([f"<li>{c}</li>" for c in certifications if c and c != "None"])
        if cert_items:
            cert_html = f'<ul class="cert-list">{cert_items}</ul>'

    # Optional sections
    projects_section = f"""
    <div class="section">
        <div class="section-title">PROJECTS</div>
        {proj_html}
    </div>""" if proj_html else ""

    certs_section = f"""
    <div class="section">
        <div class="section-title">CERTIFICATIONS</div>
        {cert_html}
    </div>""" if cert_html else ""

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{name} — Resume</title>
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');

    * {{
        margin: 0;
        padding: 0;
        box-sizing: border-box;
    }}
    
    body {{
        font-family: 'Inter', 'Segoe UI', Arial, sans-serif;
        background: #ffffff;
        color: #1a202c;
        line-height: 1.5;
        font-size: 13px;
        -webkit-font-smoothing: antialiased;
    }}

    .resume-container {{
        max-width: 800px;
        margin: 0 auto;
        padding: 40px 50px;
        background: #ffffff;
    }}

    /* ── Header ── */
    .resume-header {{
        text-align: center;
        margin-bottom: 24px;
        padding-bottom: 20px;
        border-bottom: 2px solid #1a202c;
    }}
    .resume-name {{
        font-size: 28px;
        font-weight: 700;
        letter-spacing: 3px;
        text-transform: uppercase;
        color: #1a202c;
        margin-bottom: 8px;
    }}
    .resume-contact {{
        font-size: 12px;
        color: #4a5568;
        font-weight: 400;
        letter-spacing: 0.5px;
    }}
    .resume-contact .separator {{
        margin: 0 6px;
        color: #a0aec0;
    }}

    /* ── Sections ── */
    .section {{
        margin-bottom: 20px;
    }}
    .section-title {{
        font-size: 13px;
        font-weight: 700;
        letter-spacing: 2.5px;
        text-transform: uppercase;
        color: #1a202c;
        border-bottom: 1px solid #cbd5e0;
        padding-bottom: 4px;
        margin-bottom: 12px;
    }}

    /* ── Summary ── */
    .summary-text {{
        color: #2d3748;
        font-size: 13px;
        line-height: 1.65;
        text-align: justify;
    }}

    /* ── Skills ── */
    .skill-category {{
        margin-bottom: 6px;
        line-height: 1.8;
    }}
    .skill-cat-label {{
        font-weight: 600;
        color: #1a202c;
        font-size: 12px;
    }}
    .skill-pill {{
        display: inline-block;
        background: #edf2f7;
        color: #2d3748;
        padding: 2px 10px;
        border-radius: 3px;
        font-size: 11.5px;
        font-weight: 500;
        margin: 2px 3px;
        border: 1px solid #e2e8f0;
    }}

    /* ── Experience ── */
    .job {{
        margin-bottom: 16px;
    }}
    .job-header {{
        display: flex;
        justify-content: space-between;
        align-items: flex-start;
        margin-bottom: 4px;
    }}
    .job-title {{
        font-weight: 600;
        font-size: 13.5px;
        color: #1a202c;
    }}
    .job-company {{
        font-style: italic;
        color: #4a5568;
        font-size: 12.5px;
    }}
    .job-duration {{
        font-size: 12px;
        color: #718096;
        font-weight: 500;
        white-space: nowrap;
        margin-left: 16px;
        padding-top: 2px;
    }}
    .job-bullets {{
        padding-left: 18px;
        margin-top: 4px;
    }}
    .job-bullets li {{
        color: #2d3748;
        font-size: 12.5px;
        line-height: 1.6;
        margin-bottom: 3px;
    }}

    /* ── Education ── */
    .edu-item {{
        margin-bottom: 10px;
    }}
    .edu-details {{
        color: #4a5568;
        font-size: 12px;
        margin-top: 2px;
        padding-left: 2px;
    }}

    /* ── Projects ── */
    .project-item {{
        margin-bottom: 8px;
        line-height: 1.6;
    }}
    .project-name {{
        font-weight: 600;
        color: #1a202c;
        font-size: 12.5px;
    }}
    .project-desc {{
        color: #2d3748;
        font-size: 12.5px;
    }}

    /* ── Certifications ── */
    .cert-list {{
        padding-left: 18px;
    }}
    .cert-list li {{
        color: #2d3748;
        font-size: 12.5px;
        margin-bottom: 3px;
    }}

    /* ── Print Styles ── */
    @media print {{
        body {{
            font-size: 12px;
        }}
        .resume-container {{
            padding: 20px 30px;
            max-width: 100%;
        }}
        .skill-pill {{
            border: 1px solid #ccc;
        }}
    }}
</style>
</head>
<body>
<div class="resume-container">
    <div class="resume-header">
        <div class="resume-name">{name}</div>
        <div class="resume-contact">{contact_html}</div>
    </div>

    <div class="section">
        <div class="section-title">PROFESSIONAL SUMMARY</div>
        <div class="summary-text">{summary}</div>
    </div>

    <div class="section">
        <div class="section-title">TECHNICAL SKILLS</div>
        {skills_html}
    </div>

    <div class="section">
        <div class="section-title">PROFESSIONAL EXPERIENCE</div>
        {exp_html}
    </div>

    <div class="section">
        <div class="section-title">EDUCATION</div>
        {edu_html}
    </div>

    {projects_section}
    {certs_section}
</div>
</body>
</html>"""


def render_cover_letter_html(data: dict) -> str:
    """
    Render a professional cover letter from structured data.
    
    Expected data format:
    {
        "sender_name": "John Doe",
        "sender_contact": "email@example.com | (123) 456-7890 | City, State",
        "date": "May 24, 2026",
        "recipient": "Hiring Manager",
        "company": "Company Name",
        "subject": "Application for Software Engineer Position",
        "paragraphs": [
            "Opening paragraph...",
            "Body paragraph 1...",
            "Body paragraph 2...",
            "Closing paragraph..."
        ],
        "sign_off": "Sincerely",
    }
    """
    sender_name = data.get("sender_name", "Your Name")
    sender_contact = data.get("sender_contact", "")
    date = data.get("date", "")
    recipient = data.get("recipient", "Hiring Manager")
    company = data.get("company", "")
    subject = data.get("subject", "")
    paragraphs = data.get("paragraphs", [])
    sign_off = data.get("sign_off", "Sincerely")

    paragraphs_html = "".join([f"<p>{p}</p>" for p in paragraphs])
    
    recipient_block = f"Dear {recipient},"
    if company:
        company_line = f'<div class="company-name">{company}</div>'
    else:
        company_line = ""

    subject_line = f'<div class="subject-line">Re: {subject}</div>' if subject else ""

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Cover Letter — {sender_name}</title>
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');

    * {{
        margin: 0;
        padding: 0;
        box-sizing: border-box;
    }}

    body {{
        font-family: 'Inter', 'Georgia', serif;
        background: #ffffff;
        color: #1a202c;
        line-height: 1.7;
        font-size: 14px;
        -webkit-font-smoothing: antialiased;
    }}

    .cover-letter-container {{
        max-width: 700px;
        margin: 0 auto;
        padding: 50px 60px;
        background: #ffffff;
    }}

    /* ── Sender Header ── */
    .sender-header {{
        text-align: center;
        margin-bottom: 32px;
        padding-bottom: 20px;
        border-bottom: 2px solid #1a202c;
    }}
    .sender-name {{
        font-size: 24px;
        font-weight: 700;
        letter-spacing: 2.5px;
        text-transform: uppercase;
        color: #1a202c;
        margin-bottom: 6px;
    }}
    .sender-contact-info {{
        font-size: 12px;
        color: #4a5568;
        letter-spacing: 0.5px;
    }}

    /* ── Date & Recipient ── */
    .letter-date {{
        color: #4a5568;
        font-size: 13px;
        margin-bottom: 20px;
    }}
    .company-name {{
        font-weight: 600;
        color: #2d3748;
        font-size: 13.5px;
        margin-bottom: 4px;
    }}
    .subject-line {{
        font-weight: 600;
        color: #1a202c;
        font-size: 13.5px;
        margin-bottom: 20px;
        font-style: italic;
    }}

    /* ── Salutation ── */
    .salutation {{
        font-size: 14px;
        font-weight: 500;
        color: #1a202c;
        margin-bottom: 16px;
    }}

    /* ── Body ── */
    .letter-body p {{
        color: #2d3748;
        font-size: 13.5px;
        line-height: 1.75;
        margin-bottom: 14px;
        text-align: justify;
    }}

    /* ── Sign-off ── */
    .sign-off {{
        margin-top: 28px;
    }}
    .sign-off-text {{
        color: #1a202c;
        font-size: 14px;
        font-weight: 500;
        margin-bottom: 24px;
    }}
    .sign-off-name {{
        font-size: 16px;
        font-weight: 700;
        color: #1a202c;
        letter-spacing: 0.5px;
    }}

    /* ── Print Styles ── */
    @media print {{
        .cover-letter-container {{
            padding: 30px 40px;
            max-width: 100%;
        }}
    }}
</style>
</head>
<body>
<div class="cover-letter-container">
    <div class="sender-header">
        <div class="sender-name">{sender_name}</div>
        <div class="sender-contact-info">{sender_contact}</div>
    </div>

    <div class="letter-date">{date}</div>
    {company_line}
    {subject_line}

    <div class="salutation">{recipient_block}</div>

    <div class="letter-body">
        {paragraphs_html}
    </div>

    <div class="sign-off">
        <div class="sign-off-text">{sign_off},</div>
        <div class="sign-off-name">{sender_name}</div>
    </div>
</div>
</body>
</html>"""
