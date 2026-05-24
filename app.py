"""
app.py — AI Resume Analyzer
Main Streamlit application with a premium, modern UI.
Run with: streamlit run app.py
"""

import streamlit as st
import streamlit.components.v1 as components
import json
from resume_parser import extract_text
from llm_analyzer import analyze, analyze_json
from ats_scorer import calculate_final_score
from prompts import (
    get_feedback_prompt,
    get_missing_skills_prompt,
    get_restructure_prompt,
    get_cover_letter_prompt,
    get_interview_questions_prompt,
    get_skill_recommendations_prompt,
    get_multi_resume_comparison_prompt,
)
from database import save_analysis, get_history
from html_templates import render_resume_html, render_cover_letter_html

# ─────────────────────────────────────────────
# PAGE CONFIG
# ─────────────────────────────────────────────
st.set_page_config(
    page_title="AI Resume Analyzer — Free ATS Scanner",
    page_icon="📄",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ─────────────────────────────────────────────
# SESSION STATE INIT
# ─────────────────────────────────────────────
if "loaded_analysis" not in st.session_state:
    st.session_state.loaded_analysis = None

# ─────────────────────────────────────────────
# CUSTOM CSS — Premium Dark Theme
# ─────────────────────────────────────────────
st.markdown("""
<style>
    /* ── Import Fonts ── */
    @import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@500;600;700;800&family=Outfit:wght@300;400;500;600;700;800&family=Inter:wght@300;400;500;600;700&display=swap');

    /* ── Global Styles & Animated Background ── */
    .stApp {
        font-family: 'Inter', sans-serif;
        background-color: #0B0F19; /* Midnight Base */
        background: radial-gradient(circle at 10% 20%, rgba(139, 92, 246, 0.05) 0%, transparent 40%),
                    radial-gradient(circle at 90% 80%, rgba(56, 189, 248, 0.05) 0%, transparent 40%);
        background-attachment: fixed;
        background-size: cover;
    }
    
    ::-webkit-scrollbar { width: 8px; height: 8px; }
    ::-webkit-scrollbar-track { background: transparent; }
    ::-webkit-scrollbar-thumb { background: rgba(255,255,255,0.1); border-radius: 4px; }
    ::-webkit-scrollbar-thumb:hover { background: rgba(255,255,255,0.2); }

    /* ── Animations ── */
    @keyframes fadeUp {
        0% { opacity: 0; transform: translateY(20px); }
        100% { opacity: 1; transform: translateY(0); }
    }
    @keyframes pulseGlow {
        0% { box-shadow: 0 0 0 0 rgba(139, 92, 246, 0.4); }
        70% { box-shadow: 0 0 0 10px rgba(139, 92, 246, 0); }
        100% { box-shadow: 0 0 0 0 rgba(139, 92, 246, 0); }
    }
    @keyframes gradientShift {
        0% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
        100% { background-position: 0% 50%; }
    }

    /* ── Apply Entry Animations ── */
    .stApp > header { background: transparent !important; }
    .block-container { animation: fadeUp 0.6s cubic-bezier(0.16, 1, 0.3, 1) forwards; }

    /* ── Main Header (Minimalist Glass) ── */
    .main-header {
        text-align: center;
        padding: 2rem 1.5rem;
        background: rgba(255, 255, 255, 0.02) !important;
        backdrop-filter: blur(16px) !important;
        -webkit-backdrop-filter: blur(16px) !important;
        border-radius: 16px;
        margin-bottom: 2rem;
        border: 1px solid rgba(255, 255, 255, 0.08) !important;
        box-shadow: 0 10px 30px rgba(0, 0, 0, 0.5) !important;
    }
    .main-header h1 {
        font-family: 'Inter', sans-serif;
        font-size: 2.2rem;
        font-weight: 700;
        color: #ffffff;
        margin-bottom: 0.5rem;
        letter-spacing: -0.5px;
    }
    .main-header p {
        color: #a1a1aa;
        font-size: 1.05rem;
        font-weight: 400;
        max-width: 600px;
        margin: 0 auto;
    }

    /* ── Streamlit Native UI Overrides ── */
    
    /* Primary Buttons */
    div.stButton > button:first-child {
        background: rgba(255, 255, 255, 0.05);
        color: #ffffff;
        border: 1px solid rgba(255, 255, 255, 0.15);
        backdrop-filter: blur(16px);
        padding: 0.6rem 2rem;
        border-radius: 12px;
        font-family: 'Inter', sans-serif;
        font-weight: 500;
        font-size: 1rem;
        transition: all 0.2s ease;
        box-shadow: 0 4px 14px rgba(0,0,0,0.3);
        width: 100%;
    }
    div.stButton > button:first-child:hover {
        transform: translateY(-1px);
        background: rgba(139, 92, 246, 0.15);
        box-shadow: 0 6px 20px rgba(139, 92, 246, 0.2);
        border-color: rgba(139, 92, 246, 0.4);
    }

    /* Secondary Buttons (Sidebar) */
    div[data-testid="stSidebar"] div.stButton > button:first-child {
        background: rgba(255, 255, 255, 0.03) !important;
        border: 1px solid rgba(255, 255, 255, 0.08) !important;
        backdrop-filter: blur(12px) !important;
        color: #d4d4d8 !important;
        font-size: 0.85rem !important;
        font-weight: 400 !important;
        padding: 0.4rem 0.8rem !important;
        border-radius: 8px !important;
        box-shadow: none !important;
        transition: all 0.2s ease !important;
        white-space: nowrap !important;
        overflow: hidden !important;
        text-overflow: ellipsis !important;
        display: block !important;
        width: 100% !important;
    }
    div[data-testid="stSidebar"] div.stButton > button:first-child:hover {
        background: rgba(139, 92, 246, 0.1) !important;
        border-color: rgba(139, 92, 246, 0.3) !important;
        color: white !important;
    }

    /* Inputs & Uploaders (Minimal Glass) */
    div[data-baseweb="input"], div[data-baseweb="textarea"] {
        background: rgba(0, 0, 0, 0.2) !important;
        backdrop-filter: blur(16px) !important;
        border: 1px solid rgba(255, 255, 255, 0.08) !important;
        border-radius: 10px !important;
        box-shadow: inset 0 1px 4px rgba(0,0,0,0.2) !important;
        transition: all 0.2s ease !important;
        color: white !important;
    }
    div[data-baseweb="input"]:focus-within, div[data-baseweb="textarea"]:focus-within {
        border-color: rgba(139, 92, 246, 0.5) !important;
        box-shadow: 0 0 0 1px rgba(139, 92, 246, 0.3) !important;
    }
    .stFileUploader {
        background: rgba(255, 255, 255, 0.02);
        backdrop-filter: blur(16px);
        border: 1px dashed rgba(255, 255, 255, 0.15);
        border-radius: 12px;
        padding: 1.5rem;
        transition: all 0.2s ease;
    }
    .stFileUploader:hover {
        border-color: rgba(139, 92, 246, 0.4);
        background: rgba(139, 92, 246, 0.02);
    }

    /* Tabs */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
        background-color: rgba(24, 24, 27, 0.5);
        padding: 0.5rem;
        border-radius: 16px;
        border: 1px solid rgba(255, 255, 255, 0.05);
    }
    .stTabs [data-baseweb="tab"] {
        border-radius: 10px;
        padding: 10px 20px;
        font-family: 'Outfit', sans-serif;
        font-weight: 500;
        color: #a1a1aa;
        border: none !important;
        background-color: transparent;
        transition: all 0.2s ease;
    }
    .stTabs [aria-selected="true"] {
        background-color: rgba(255, 255, 255, 0.1) !important;
        color: white !important;
        box-shadow: 0 4px 12px rgba(0,0,0,0.1);
    }
    .stTabs [data-baseweb="tab-highlight"] { display: none; }

    /* ── Metric Cards & History Cards (Minimal Glass) ── */
    .score-card, .history-card {
        background: rgba(255, 255, 255, 0.02) !important;
        backdrop-filter: blur(16px) !important;
        -webkit-backdrop-filter: blur(16px) !important;
        border: 1px solid rgba(255, 255, 255, 0.08) !important;
        border-radius: 16px;
        box-shadow: 0 10px 30px rgba(0,0,0,0.3) !important;
        transition: all 0.3s ease;
    }
    .score-card {
        border-radius: 20px;
        padding: 2.5rem;
        text-align: center;
        position: relative;
        overflow: hidden;
    }
    .score-card::after {
        content: ''; position: absolute; top: 0; left: -100%; width: 50%; height: 100%;
        background: linear-gradient(to right, transparent, rgba(255,255,255,0.04), transparent);
        transform: skewX(-20deg); transition: 0.6s;
    }
    .score-card:hover {
        transform: translateY(-4px);
        border-color: rgba(139, 92, 246, 0.3) !important;
        box-shadow: 0 15px 40px rgba(139, 92, 246, 0.15) !important;
    }
    .score-number {
        font-family: 'Inter', sans-serif;
        font-size: 4.5rem;
        font-weight: 800;
        line-height: 1;
        margin-bottom: 0.5rem;
        text-shadow: 0 4px 20px rgba(0,0,0,0.5);
    }
    .score-label {
        color: #94a3b8;
        font-size: 0.95rem;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 2px;
    }
    .score-green { color: #10b981; text-shadow: 0 0 30px rgba(16, 185, 129, 0.5); }
    .score-orange { color: #f59e0b; text-shadow: 0 0 30px rgba(245, 158, 11, 0.5); }
    .score-red { color: #ef4444; text-shadow: 0 0 30px rgba(239, 68, 68, 0.5); }

    .history-card {
        border-radius: 12px;
        padding: 1.2rem;
        margin-bottom: 0.8rem;
    }
    .history-card:hover {
        border-color: rgba(139, 92, 246, 0.4) !important;
        background: rgba(255, 255, 255, 0.05) !important;
        transform: translateX(4px);
    }
    
    .history-filename { 
        font-family: 'Inter', sans-serif; 
        font-weight: 500; 
        color: #e2e8f0; 
        font-size: 0.9rem;
        white-space: nowrap;
        overflow: hidden;
        text-overflow: ellipsis;
        display: block;
        width: 100%;
    }
    .history-date { color: #64748b; font-size: 0.75rem; margin-top: 2px; }
    .history-score { font-family: 'Inter', sans-serif; font-weight: 700; font-size: 1.1rem; }
    /* ── Breakdown Cards ── */
    .breakdown-item {
        background: rgba(255, 255, 255, 0.02);
        border: 1px solid rgba(255, 255, 255, 0.05);
        border-radius: 14px;
        padding: 1.2rem 1.5rem;
        margin-bottom: 0.8rem;
        display: flex;
        justify-content: space-between;
        align-items: center;
        transition: all 0.2s ease;
    }
    .breakdown-item:hover {
        background: rgba(255, 255, 255, 0.05);
        transform: translateX(4px);
        border-color: rgba(139, 92, 246, 0.3);
    }
    .breakdown-label {
        color: #d4d4d8;
        font-family: 'Outfit', sans-serif;
        font-weight: 500;
        font-size: 1.05rem;
    }
    .breakdown-value {
        font-family: 'Outfit', sans-serif;
        font-weight: 700;
        font-size: 1.2rem;
        background: rgba(0,0,0,0.2);
        padding: 0.3rem 1rem;
        border-radius: 20px;
    }

    /* ── Skill Tags ── */
    .skill-found, .skill-missing {
        display: inline-block;
        padding: 0.5rem 1.2rem;
        border-radius: 30px;
        margin: 0.3rem;
        font-size: 0.9rem;
        font-weight: 600;
        transition: all 0.2s ease;
        backdrop-filter: blur(4px);
    }
    .skill-found {
        background: rgba(16, 185, 129, 0.1);
        color: #10b981;
        border: 1px solid rgba(16, 185, 129, 0.2);
    }
    .skill-found:hover { background: rgba(16, 185, 129, 0.2); transform: scale(1.05); }

    .skill-missing {
        background: rgba(239, 68, 68, 0.1);
        color: #ef4444;
        border: 1px solid rgba(239, 68, 68, 0.2);
    }
    .skill-missing:hover { background: rgba(239, 68, 68, 0.2); transform: scale(1.05); }

    /* ── History Cards ── */
    .history-card {
        background: rgba(24, 24, 27, 0.6);
        border: 1px solid rgba(255, 255, 255, 0.05);
        border-radius: 12px;
        padding: 1.2rem;
        margin-bottom: 0.5rem;
        transition: all 0.2s ease;
    }
    .history-card:hover {
        background: rgba(255, 255, 255, 0.05);
        border-color: rgba(139, 92, 246, 0.4);
    }
    .history-filename { font-family: 'Outfit', sans-serif; font-weight: 600; color: #f4f4f5; font-size: 0.95rem; }
    .history-date { color: #a1a1aa; font-size: 0.8rem; margin-top: 4px; }
    .history-score { font-family: 'Outfit', sans-serif; font-weight: 800; font-size: 1.3rem; }

    /* ── Section Headers ── */
    .section-header {
        font-family: 'Inter', sans-serif;
        font-size: 1.3rem;
        font-weight: 600;
        color: #f8fafc;
        margin-bottom: 1rem;
        display: flex;
        align-items: center;
        gap: 10px;
    }
    .section-header::after {
        content: ''; flex: 1; height: 1px;
        background: linear-gradient(to right, rgba(255,255,255,0.05), transparent);
    }
    
    /* ── Course Cards ── */
    .course-card {
        background: rgba(255, 255, 255, 0.02);
        border-left: 3px solid #8b5cf6;
        padding: 1.2rem;
        margin-bottom: 1rem;
        border-radius: 0 12px 12px 0;
        border-top: 1px solid rgba(255,255,255,0.05);
        border-right: 1px solid rgba(255,255,255,0.05);
        border-bottom: 1px solid rgba(255,255,255,0.05);
        transition: transform 0.2s ease, background 0.2s ease;
    }
    .course-card:hover {
        transform: translateX(4px);
        background: rgba(255, 255, 255, 0.04);
    }
</style>
""", unsafe_allow_html=True)


# ─────────────────────────────────────────────
# SIDEBAR
# ─────────────────────────────────────────────
with st.sidebar:
    st.markdown("### ⚙️ Mode Selection")
    app_mode = st.radio(
        "Choose Analysis Mode:",
        ["Single Resume Analysis", "Multi-Resume Comparison"],
        help="Single mode gives deep feedback. Multi mode ranks candidates for HR."
    )
    
    st.markdown("---")
    st.markdown("### 📂 Analysis History")

    history = get_history(limit=15)

    if not history:
        st.markdown(
            '<p style="color:#718096; font-size:0.9rem;">No analyses yet. Upload a resume to get started!</p>',
            unsafe_allow_html=True,
        )
    else:
        for record in history:
            score = record.get("ats_score", 0)
            color_class = "score-green" if score >= 75 else ("score-orange" if score >= 50 else "score-red")
            date_str = record["created_at"][:10] if record.get("created_at") else "Unknown"

            st.markdown(f"""
            <div class="history-card">
                <div style="display:flex; justify-content:space-between; align-items:center; gap: 8px;">
                    <div style="flex: 1; min-width: 0; overflow: hidden;">
                        <div class="history-filename" title="{record.get('filename', 'Unknown')}">📄 {record.get('filename', 'Unknown')}</div>
                        <div class="history-date">{date_str}</div>
                    </div>
                    <div class="history-score {color_class}" style="flex-shrink: 0;">{score}/100</div>
                </div>
            </div>
            """, unsafe_allow_html=True)
            
            if st.button(f"Load '{record.get('filename', 'Unknown')}'", key=f"load_history_{record.get('id')}", use_container_width=True):
                st.session_state.loaded_analysis = record
                # Ensure we are in single resume mode to view the record
                app_mode = "Single Resume Analysis"
                st.rerun()

    st.markdown("---")
    st.markdown(
        '<p style="color:#4a5568; font-size:0.75rem; text-align:center;">'
        "Powered by Groq • Llama 3.3 70B<br>100% Free • No data stored externally</p>",
        unsafe_allow_html=True,
    )


# ─────────────────────────────────────────────
# MAIN HEADER
# ─────────────────────────────────────────────
st.markdown("""
<div class="main-header">
    <h1>📄 AI Resume Analyzer</h1>
    <p>Get instant ATS scoring, detailed feedback, skill gaps, cover letters, and interview prep.</p>
</div>
""", unsafe_allow_html=True)


# ─────────────────────────────────────────────
# MODE: SINGLE RESUME
# ─────────────────────────────────────────────
if app_mode == "Single Resume Analysis":
    
    # If a history record is loaded, offer a way to clear it
    if st.session_state.loaded_analysis:
        st.success(f"📂 Viewing past analysis for: **{st.session_state.loaded_analysis.get('filename')}**")
        if st.button("➕ Start New Analysis", type="secondary"):
            st.session_state.loaded_analysis = None
            st.rerun()
            
    else:
        col_upload, col_jd = st.columns(2, gap="large")

        with col_upload:
            st.markdown('<div class="section-header">📎 Upload Your Resume</div>', unsafe_allow_html=True)
            uploaded_file = st.file_uploader(
                "Upload PDF or DOCX",
                type=["pdf", "docx"],
                label_visibility="collapsed",
                help="Supports PDF and DOCX formats. Max 10MB.",
                key="resume_uploader",
            )
            if uploaded_file:
                st.success(f"✅ Uploaded: **{uploaded_file.name}** ({round(uploaded_file.size / 1024, 1)} KB)")

        with col_jd:
            st.markdown('<div class="section-header">🎯 Paste Job Description</div>', unsafe_allow_html=True)
            job_description = st.text_area(
                "Paste the job description here",
                height=200,
                placeholder="Paste the full job description here...\n\nThis helps the AI compare your resume against the specific role requirements for accurate ATS scoring and skill gap analysis.",
                label_visibility="collapsed",
                key="job_description_input",
            )

        st.markdown("")
        col_btn_left, col_btn_center, col_btn_right = st.columns([1, 2, 1])
        with col_btn_center:
            analyze_clicked = st.button(
                "🚀 Run Full AI Analysis",
                use_container_width=True,
                type="primary",
                key="analyze_button",
            )

        if analyze_clicked:
            if not uploaded_file:
                st.warning("⚠️ Please upload your resume (PDF or DOCX) first.")
                st.stop()
            if not job_description or len(job_description.strip()) < 20:
                st.warning("⚠️ Please paste a complete job description (at least a few sentences).")
                st.stop()

            with st.spinner("🔍 Extracting text from your resume..."):
                resume_text = extract_text(uploaded_file)

            if resume_text.startswith("❌"):
                st.error(resume_text)
                st.stop()

            progress = st.progress(0, text="Starting AI analysis...")

            progress.progress(10, text="📝 Generating detailed feedback...")
            feedback = analyze(get_feedback_prompt(resume_text))

            progress.progress(25, text="📊 Calculating ATS compatibility score...")
            score_result = calculate_final_score(resume_text, job_description)

            progress.progress(40, text="🔍 Analyzing skill gaps...")
            skills_prompt = get_missing_skills_prompt(resume_text, job_description)
            skills_data = analyze_json(skills_prompt, max_tokens=1500) or {"found": [], "missing": []}

            progress.progress(55, text="✨ Rewriting your resume...")
            resume_json = analyze_json(get_restructure_prompt(resume_text, job_description), max_tokens=4000)
            if resume_json:
                improved_resume = render_resume_html(resume_json)
            else:
                improved_resume = "<p>Failed to generate improved resume. Please try again.</p>"

            progress.progress(70, text="✉️ Generating custom cover letter...")
            cover_json = analyze_json(get_cover_letter_prompt(resume_text, job_description), max_tokens=2000)
            if cover_json:
                cover_letter = render_cover_letter_html(cover_json)
            else:
                cover_letter = "<p>Failed to generate cover letter. Please try again.</p>"

            progress.progress(80, text="🎙️ Preparing interview questions...")
            interview_qs = analyze(get_interview_questions_prompt(resume_text, job_description), max_tokens=2500)

            progress.progress(90, text="📚 Finding recommended courses...")
            courses_prompt = get_skill_recommendations_prompt(resume_text, job_description)
            courses_data = analyze_json(courses_prompt, max_tokens=2500) or {"priority_skills": [], "learning_path": ""}

            progress.progress(95, text="💾 Saving analysis...")
            record_id = save_analysis(
                filename=uploaded_file.name,
                ats_score=score_result["final_score"],
                missing_skills=skills_data.get("missing", []),
                feedback=feedback,
                improved_resume=improved_resume,
                cover_letter=cover_letter,
                interview_questions=interview_qs,
                skill_recommendations=json.dumps(courses_data),
            )
            
            # Pack all the results into a dict matching the database structure so we can view it
            st.session_state.loaded_analysis = {
                "id": record_id,
                "filename": uploaded_file.name,
                "ats_score": score_result["final_score"],
                "missing_skills": skills_data.get("missing", []),
                "feedback": feedback,
                "improved_resume": improved_resume,
                "cover_letter": cover_letter,
                "interview_questions": interview_qs,
                "skill_recommendations": json.dumps(courses_data),
                "created_at": "Just now",
                # The rule checks and AI breakdown aren't fully saved to DB right now, 
                # but we'll store them temporarily in session state so the view works immediately after generation
                "_temporary_score_result": score_result,
                "_temporary_skills_data": skills_data,
            }

            progress.progress(100, text="✅ Analysis complete!")
            st.rerun() # Rerun to display the loaded analysis

    # Render results if we have a loaded analysis (either from history or just generated)
    if st.session_state.loaded_analysis:
        record = st.session_state.loaded_analysis
        
        # ─────────────────────────────────────────
        # RESULTS TABS
        # ─────────────────────────────────────────
        st.markdown("---")
        st.markdown("""
        <div style="text-align:center; margin: 1.5rem 0;">
            <h2 style="font-weight:700; color:#e2e8f0;">📊 Comprehensive Analysis Results</h2>
        </div>
        """, unsafe_allow_html=True)

        tabs = st.tabs([
            "📊 ATS Score",
            "📝 Feedback",
            "🔍 Skills Gap",
            "✨ Improved Resume",
            "✉️ Cover Letter",
            "🎙️ Interview Prep",
            "📚 Learning Paths",
        ])

        # Extract data from the record
        final_score = record.get("ats_score", 0)
        feedback = record.get("feedback", "")
        improved_resume = record.get("improved_resume", "")
        cover_letter = record.get("cover_letter", "")
        interview_qs = record.get("interview_questions", "")
        
        missing_skills = record.get("missing_skills", [])
        if isinstance(missing_skills, str):
            try:
                missing_skills = json.loads(missing_skills)
            except:
                missing_skills = []
                
        skill_recs_raw = record.get("skill_recommendations", "{}")
        if isinstance(skill_recs_raw, str):
            try:
                courses_data = json.loads(skill_recs_raw)
            except:
                courses_data = {"priority_skills": [], "learning_path": ""}
        else:
            courses_data = skill_recs_raw

        # TAB 1 — ATS SCORE
        with tabs[0]:
            if final_score >= 75:
                score_color, score_emoji, score_msg = "score-green", "🟢", "Excellent! Your resume is well-optimized."
            elif final_score >= 50:
                score_color, score_emoji, score_msg = "score-orange", "🟡", "Good foundation, room for improvement."
            else:
                score_color, score_emoji, score_msg = "score-red", "🔴", "Needs significant improvement."

            col_score, col_breakdown = st.columns([1, 2], gap="large")
            with col_score:
                st.markdown(f"""
                <div class="score-card">
                    <div class="score-number {score_color}">{final_score}</div>
                    <div class="score-label">ATS Score / 100</div>
                    <div style="margin-top:1rem; font-size:0.95rem; color:#a0aec0;">{score_emoji} {score_msg}</div>
                </div>
                """, unsafe_allow_html=True)
                st.markdown("")
                st.progress(final_score / 100)
                
                # Check if we have the temporary full breakdown
                if "_temporary_score_result" in record:
                    score_result = record["_temporary_score_result"]
                    st.markdown(f"""
                    <div style="margin-top:1rem;">
                        <div class="breakdown-item"><span class="breakdown-label">🔧 Rule-Based Score</span><span class="breakdown-value" style="color:#667eea;">{score_result['rule_score']}/{score_result['rule_max']}</span></div>
                        <div class="breakdown-item"><span class="breakdown-label">🤖 AI Analysis Score</span><span class="breakdown-value" style="color:#764ba2;">{score_result['ai_score_normalized']}/{score_result['ai_max']}</span></div>
                    </div>
                    """, unsafe_allow_html=True)

            with col_breakdown:
                if "_temporary_score_result" in record:
                    st.markdown('<div class="section-header">AI Breakdown</div>', unsafe_allow_html=True)
                    ai_bd = score_result["ai_breakdown"]
                    for label, value in [("🔑 Keyword Match", ai_bd.get("keyword_match", "N/A")), ("📐 Formatting", ai_bd.get("formatting_score", "N/A")), ("⚡ Skills Match", ai_bd.get("skills_match", "N/A")), ("💼 Experience Relevance", ai_bd.get("experience_relevance", "N/A")), ("📋 Structure", ai_bd.get("structure_score", "N/A"))]:
                        val_color = "#48bb78" if isinstance(value, (int, float)) and value >= 75 else ("#ed8936" if isinstance(value, (int, float)) and value >= 50 else "#fc8181") if isinstance(value, (int, float)) else "#718096"
                        display_val = f"{value}/100" if isinstance(value, (int, float)) else str(value)
                        st.markdown(f'<div class="breakdown-item"><span class="breakdown-label">{label}</span><span class="breakdown-value" style="color:{val_color};">{display_val}</span></div>', unsafe_allow_html=True)
                    
                    st.markdown('<div class="section-header" style="margin-top:1.5rem;">Rule-Based Checks</div>', unsafe_allow_html=True)
                    for key, check in score_result["rule_checks"].items():
                        if check["passed"]: st.markdown(f'<div class="check-pass">✅ {check["label"]} (+{check["points"]} pts)</div>', unsafe_allow_html=True)
                        else: st.markdown(f'<div class="check-fail">❌ {check["label"]} (0/{check["points"]} pts)</div>', unsafe_allow_html=True)
                else:
                    st.info("ℹ️ Detailed score breakdown is only available immediately after running a new analysis. Overall score is saved.")

        # TAB 2 — FEEDBACK
        with tabs[1]:
            st.markdown('<div class="section-header">📝 Detailed Resume Feedback</div>', unsafe_allow_html=True)
            st.markdown(feedback)

        # TAB 3 — SKILLS GAP
        with tabs[2]:
            st.markdown('<div class="section-header">🔍 Skills Gap Analysis</div>', unsafe_allow_html=True)
            col_found, col_missing = st.columns(2, gap="large")
            with col_found:
                if "_temporary_skills_data" in record:
                    found = record["_temporary_skills_data"].get("found", [])
                    st.markdown(f"**✅ Found in Your Resume** ({len(found)} skills)")
                    if found: st.markdown(f'<div style="margin-top:0.5rem;">{"".join([f"<span class=skill-found>✔ {s}</span>" for s in found])}</div>', unsafe_allow_html=True)
                    else: st.info("No matching skills were detected.")
                else:
                    st.info("Found skills details are only available immediately after running an analysis. Missing skills are saved below.")
            with col_missing:
                st.markdown(f"**❌ Missing from Your Resume** ({len(missing_skills)} skills)")
                if missing_skills: st.markdown(f'<div style="margin-top:0.5rem;">{"".join([f"<span class=skill-missing>✘ {s}</span>" for s in missing_skills])}</div>', unsafe_allow_html=True)
                else: st.success("🎉 Great! No critical skills are missing.")

        # TAB 4 — IMPROVED RESUME
        with tabs[3]:
            st.markdown('<div class="section-header">✨ Professionally Restructured Resume</div>', unsafe_allow_html=True)
            if improved_resume:
                components.html(improved_resume, height=900, scrolling=True)
                
                col_dl1, col_dl2 = st.columns(2)
                with col_dl1:
                    st.download_button(
                        "📥 Download as HTML", 
                        improved_resume, 
                        f"improved_{record.get('filename', 'resume')}.html", 
                        "text/html", 
                        key="dl_improved",
                        use_container_width=True
                    )
                with col_dl2:
                    # Extract plain text from the HTML for a .txt download option
                    import re
                    plain_text = re.sub(r'<[^>]+>', '', improved_resume)
                    plain_text = re.sub(r'\s+', ' ', plain_text).strip()
                    st.download_button(
                        "📄 Download as Text",
                        plain_text,
                        f"improved_{record.get('filename', 'resume')}.txt",
                        "text/plain",
                        key="dl_improved_txt",
                        use_container_width=True
                    )
                st.markdown("<p style='font-size:0.8rem; color:#a0aec0; text-align:center;'>💡 Open the HTML file in your browser → Press Ctrl+P → Save as PDF for a perfect printable resume.</p>", unsafe_allow_html=True)
            else:
                st.info("No improved resume saved for this record.")

        # TAB 5 — COVER LETTER
        with tabs[4]:
            st.markdown('<div class="section-header">✉️ Professional Cover Letter</div>', unsafe_allow_html=True)
            if cover_letter:
                components.html(cover_letter, height=700, scrolling=True)
                
                col_dl3, col_dl4 = st.columns(2)
                with col_dl3:
                    st.download_button(
                        "📥 Download as HTML", 
                        cover_letter, 
                        f"cover_letter_{record.get('filename', 'resume')}.html", 
                        "text/html", 
                        key="dl_cover",
                        use_container_width=True
                    )
                with col_dl4:
                    import re
                    plain_cl = re.sub(r'<[^>]+>', '', cover_letter)
                    plain_cl = re.sub(r'\s+', ' ', plain_cl).strip()
                    st.download_button(
                        "📄 Download as Text",
                        plain_cl,
                        f"cover_letter_{record.get('filename', 'resume')}.txt",
                        "text/plain",
                        key="dl_cover_txt",
                        use_container_width=True
                    )
            else:
                st.info("No cover letter saved for this record.")

        # TAB 6 — INTERVIEW PREP
        with tabs[5]:
            st.markdown('<div class="section-header">🎙️ Interview Preparation</div>', unsafe_allow_html=True)
            if interview_qs:
                st.markdown(interview_qs)
            else:
                st.info("No interview questions saved for this record.")
            
        # TAB 7 — LEARNING PATHS
        with tabs[6]:
            st.markdown('<div class="section-header">📚 Suggested Learning Paths</div>', unsafe_allow_html=True)
            
            if "learning_path" in courses_data and courses_data["learning_path"]:
                st.info(f"💡 **Strategy:** {courses_data['learning_path']}")
                
            skills = courses_data.get("priority_skills", [])
            if not skills:
                st.success("You have a very strong skill match! No specific courses needed right now, or no recommendations were saved.")
            else:
                for skill in skills:
                    st.markdown(f"#### 🎯 Skill: **{skill.get('skill', 'Unknown')}** (Priority: {skill.get('importance', 'Medium')})")
                    for course in skill.get("free_courses", []):
                        st.markdown(f"""
                        <div class="course-card">
                            <strong>📚 {course.get('name', 'Course')}</strong> — <i>{course.get('platform', 'Platform')}</i><br>
                            <a href="{course.get('url', '#')}" target="_blank" style="color:#667eea; text-decoration:none;">🔗 Link to course</a> • ⏱️ {course.get('duration', 'Unknown duration')}
                        </div>
                        """, unsafe_allow_html=True)
                    for cert in skill.get("certifications", []):
                        st.markdown(f"""
                        <div class="course-card" style="border-left-color: #ed8936;">
                            <strong>🏆 Certification: {cert.get('name', 'Cert')}</strong> — <i>{cert.get('provider', 'Provider')}</i><br>
                            <a href="{cert.get('url', '#')}" target="_blank" style="color:#ed8936; text-decoration:none;">🔗 View Certification</a> • 💰 {cert.get('cost', 'Unknown')}
                        </div>
                        """, unsafe_allow_html=True)

# ─────────────────────────────────────────────
# MODE: MULTI-RESUME COMPARISON
# ─────────────────────────────────────────────
else:
    st.markdown("### 👥 Bulk Candidate Evaluation")
    st.markdown("Upload multiple resumes to see who fits the job description best.")
    
    col_upload_m, col_jd_m = st.columns(2, gap="large")

    with col_upload_m:
        st.markdown('<div class="section-header">📎 Upload Resumes</div>', unsafe_allow_html=True)
        uploaded_files = st.file_uploader(
            "Upload multiple PDFs or DOCXs",
            type=["pdf", "docx"],
            accept_multiple_files=True,
            label_visibility="collapsed",
            key="multi_resume_uploader",
        )
        if uploaded_files:
            st.success(f"✅ Uploaded **{len(uploaded_files)}** candidate resumes.")

    with col_jd_m:
        st.markdown('<div class="section-header">🎯 Paste Job Description</div>', unsafe_allow_html=True)
        job_description_m = st.text_area(
            "Paste the job description here",
            height=200,
            placeholder="Paste the full job description here...",
            label_visibility="collapsed",
            key="multi_job_description",
        )
        
    st.markdown("")
    col_btn_m_left, col_btn_m_center, col_btn_m_right = st.columns([1, 2, 1])
    with col_btn_m_center:
        compare_clicked = st.button(
            "⚖️ Rank Candidates",
            use_container_width=True,
            type="primary",
            key="compare_button",
        )

    if compare_clicked:
        if len(uploaded_files) < 2:
            st.warning("⚠️ Please upload at least 2 resumes to compare.")
            st.stop()
        if not job_description_m or len(job_description_m.strip()) < 20:
            st.warning("⚠️ Please paste a complete job description.")
            st.stop()

        with st.spinner("🔍 Extracting text from all resumes..."):
            resumes_dict = {}
            for file in uploaded_files:
                text = extract_text(file)
                if not text.startswith("❌"):
                    resumes_dict[file.name] = text

        if not resumes_dict:
            st.error("❌ Failed to extract readable text from any uploaded files.")
            st.stop()
            
        with st.spinner("⚖️ AI is analyzing and ranking candidates... (This may take a minute)"):
            prompt = get_multi_resume_comparison_prompt(resumes_dict, job_description_m)
            ranking_data = analyze_json(prompt, max_retries=2)
            
        if ranking_data and "rankings" in ranking_data:
            st.markdown("---")
            st.markdown("### 🏆 Candidate Rankings")
            
            for rank_item in ranking_data["rankings"]:
                rank = rank_item.get("rank")
                filename = rank_item.get("filename")
                score = rank_item.get("score")
                justification = rank_item.get("justification")
                
                medal = "🥇" if rank == 1 else "🥈" if rank == 2 else "🥉" if rank == 3 else f"#{rank}"
                color = "score-green" if score >= 80 else ("score-orange" if score >= 60 else "score-red")
                
                st.markdown(f"""
                <div class="score-card" style="text-align: left; padding: 1.5rem; margin-bottom: 1rem; display: flex; align-items: center; justify-content: space-between;">
                    <div style="flex: 1;">
                        <h3 style="margin-top: 0; margin-bottom: 0.5rem; color: #e2e8f0;">{medal} {filename}</h3>
                        <p style="margin: 0; color: #a0aec0; font-size: 0.95rem;">{justification}</p>
                    </div>
                    <div style="text-align: right; margin-left: 2rem;">
                        <div class="score-number {color}" style="font-size: 2.5rem; margin-bottom: 0;">{score}</div>
                        <div class="score-label" style="font-size: 0.75rem;">Match Score</div>
                    </div>
                </div>
                """, unsafe_allow_html=True)
        else:
            st.error("❌ Failed to generate rankings. The AI model returned an invalid response. Try slightly reducing the job description length.")
