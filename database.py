"""
database.py — SQLite database for persisting analysis history.
Zero setup, zero cost — the DB file is created automatically.
"""

import sqlite3
import json
from datetime import datetime

DB_FILE = "analyses.db"


def _get_connection():
    """Get a database connection, creating the table if it doesn't exist."""
    conn = sqlite3.connect(DB_FILE)
    conn.row_factory = sqlite3.Row

    # Create main analyses table
    conn.execute("""
        CREATE TABLE IF NOT EXISTS analyses (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            filename TEXT NOT NULL,
            ats_score INTEGER DEFAULT 0,
            missing_skills TEXT DEFAULT '[]',
            feedback TEXT DEFAULT '',
            improved_resume TEXT DEFAULT '',
            cover_letter TEXT DEFAULT '',
            interview_questions TEXT DEFAULT '',
            skill_recommendations TEXT DEFAULT '',
            created_at TEXT NOT NULL
        )
    """)
    conn.commit()
    return conn


def save_analysis(
    filename: str,
    ats_score: int,
    missing_skills: list,
    feedback: str,
    improved_resume: str,
    cover_letter: str = "",
    interview_questions: str = "",
    skill_recommendations: str = "",
) -> int:
    """
    Save a completed analysis to the database.
    
    Returns:
        The row ID of the saved record.
    """
    conn = _get_connection()
    try:
        cursor = conn.execute(
            """
            INSERT INTO analyses (filename, ats_score, missing_skills, feedback, improved_resume, 
                                  cover_letter, interview_questions, skill_recommendations, created_at)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                filename,
                ats_score,
                json.dumps(missing_skills),
                feedback,
                improved_resume,
                cover_letter,
                interview_questions,
                json.dumps(skill_recommendations) if isinstance(skill_recommendations, dict) else skill_recommendations,
                datetime.now().isoformat(),
            ),
        )
        conn.commit()
        return cursor.lastrowid
    finally:
        conn.close()


def get_history(limit: int = 20) -> list[dict]:
    """
    Fetch past analyses, most recent first.
    
    Args:
        limit: Maximum number of records to return.
        
    Returns:
        List of analysis records as dictionaries.
    """
    conn = _get_connection()
    try:
        rows = conn.execute(
            "SELECT * FROM analyses ORDER BY created_at DESC LIMIT ?",
            (limit,),
        ).fetchall()

        results = []
        for row in rows:
            record = dict(row)
            # Parse the JSON string back to a list
            try:
                record["missing_skills"] = json.loads(record["missing_skills"])
            except (json.JSONDecodeError, TypeError):
                record["missing_skills"] = []
            results.append(record)

        return results
    finally:
        conn.close()


def delete_analysis(record_id: int) -> bool:
    """Delete a specific analysis record by ID."""
    conn = _get_connection()
    try:
        conn.execute("DELETE FROM analyses WHERE id = ?", (record_id,))
        conn.commit()
        return True
    finally:
        conn.close()
