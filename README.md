# 🌌 Resumify — Premium AI Resume Analyzer & Optimizer

Resumify is a high-end, hyper-modern SaaS-style AI Resume Analyzer designed to optimize resumes for Applicant Tracking Systems (ATS) and provide actionable, intelligent feedback. Powered by the state-of-the-art **Llama 3.3 70B** model on **Groq API**, it features a beautiful, ultra-minimalistic glassmorphism design optimized for visual precision and corporate standards.

---

## 🚀 Key Features

*   **📊 ATS Score & Compatibility:** Uses a hybrid rule-based and AI-powered scoring system to evaluate how ATS-friendly your resume is.
*   **🔍 Detailed Feedback & Gap Analysis:** Reviews formatting, grammar, and achievements, offering checkmark/cross bullet points for areas of improvement.
*   **💡 Missing Skills Detection:** Compares the uploaded resume against a pasted Job Description to highlight crucial missing technical and soft skills.
*   **✨ Professional Resume Restructuring:** Intelligently restructures and rewrites weak bullet points, rendering a beautiful, professional, printable HTML template.
*   **✉️ Custom Cover Letter Generator:** Drafts a highly tailored corporate cover letter mapped specifically to the job role.
*   **🎙️ Interactive Interview Prep:** Generates customized technical and behavioral (STAR method) interview questions based on the candidate's experience.
*   **📚 Personalized Learning Paths:** Recommends specific, free online courses and certifications to bridge identified skill gaps.
*   **📂 Persistent Local History:** Keeps track of previous analysis history stored securely in a local SQLite database so you never lose your progress.
*   **👥 HR Mode (Multi-Resume Comparison):** Enables recruiters to upload multiple resumes to compare and rank candidates for a job description side-by-side.

---

## 🛠️ Technology Stack

*   **Frontend UI:** [Streamlit](https://streamlit.io/) heavily customized with a bespoke, minimalistic **Glassmorphism CSS Engine** (featuring `#0B0F19` midnight palette, 1px silver border aesthetics, and layout overflow handling).
*   **LLM Core:** [Groq API](https://groq.com/) using the ultra-fast `llama-3.3-70b-versatile` model.
*   **Parser Module:** `pdfplumber` (for ultra-accurate PDF text extraction) and `python-docx` (for Word documents).
*   **Database:** SQLite (local persistence).

---

## 📦 Installation & Local Setup

### 1. Clone or Download the Project
Download this project directory or clone it from GitHub:
```bash
git clone https://github.com/yourusername/ai-resume-analyzer.git
cd ai-resume-analyzer
```

### 2. Set Up Virtual Environment (Recommended)
```bash
# Create a virtual environment
python -m venv venv

# Activate it (Windows)
venv\Scripts\activate

# Activate it (macOS/Linux)
source venv/bin/activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Configure Environment Variables
Create a file named `.env` in the root directory of your project and add your Groq API key:
```env
GROQ_API_KEY="your_groq_api_key_here"
```
> **Note:** Get a free API key from [Groq Console](https://console.groq.com/).

### 5. Launch the Web Application
```bash
streamlit run app.py
```

---

## 🌐 Free Cloud Deployment (Streamlit Community Cloud)

Resumify is fully optimized for **Streamlit Community Cloud** deployment:

1.  Push your project files to a GitHub repository (do **not** push `.env` or `venv/`).
2.  Log in to [Streamlit Community Cloud](https://share.streamlit.io/).
3.  Click **New app**, select your repository, select `app.py` as your main file path.
4.  Open **Advanced Settings** -> **Secrets** and add your Groq key:
    ```toml
    GROQ_API_KEY="your_groq_api_key_here"
    ```
5.  Click **Deploy**!

---

## 📄 License
This project is open-source and free to use for semester projects, hackathons, and portfolios.
