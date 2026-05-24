"""
llm_analyzer.py — Handles all communication with the Groq API.
Uses Llama 3.3 70B (free tier) for resume analysis.
"""

import os
import json
import re
from groq import Groq
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Initialize Groq client
_client = None


def _get_client() -> Groq:
    """Lazy-initialize the Groq client."""
    global _client
    if _client is None:
        api_key = os.getenv("GROQ_API_KEY")
        if not api_key or api_key == "your_groq_key_here":
            raise ValueError(
                "⚠️ GROQ_API_KEY not set. Please add your API key to the .env file.\n"
                "Get a free key at: https://console.groq.com/keys"
            )
        _client = Groq(api_key=api_key)
    return _client


def analyze(prompt: str, max_tokens: int = 2000, temperature: float = 0.3) -> str:
    """
    Send a prompt to Groq's Llama 3.3 70B model and return the response text.

    Args:
        prompt: The fully formatted prompt string.
        max_tokens: Maximum response length (default 2000).
        temperature: Creativity level — 0.3 for consistent professional output.

    Returns:
        The model's response text, or an error message.
    """
    try:
        client = _get_client()
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {
                    "role": "system",
                    "content": "You are a professional resume analysis AI. Provide accurate, detailed, and actionable insights.",
                },
                {
                    "role": "user",
                    "content": prompt,
                },
            ],
            max_tokens=max_tokens,
            temperature=temperature,
        )
        return response.choices[0].message.content.strip()

    except ValueError as e:
        return str(e)
    except Exception as e:
        return f"❌ API Error: {str(e)}"


def analyze_json(prompt: str, max_retries: int = 2, max_tokens: int = 2000) -> dict | None:
    """
    Send a prompt expecting a JSON response. Parses and validates the output.
    Retries up to max_retries times if JSON parsing fails.

    Args:
        prompt: The fully formatted prompt expecting JSON output.
        max_retries: Number of retry attempts on parse failure.
        max_tokens: Maximum tokens for the response.

    Returns:
        Parsed dictionary, or None if all attempts fail.
    """
    for attempt in range(max_retries + 1):
        response_text = analyze(prompt, max_tokens=max_tokens, temperature=0.1)

        # Check for error messages
        if response_text.startswith("❌") or response_text.startswith("⚠️"):
            return None

        # Clean up common LLM artifacts
        cleaned = _clean_json_response(response_text)

        try:
            result = json.loads(cleaned)
            if isinstance(result, dict):
                return result
        except json.JSONDecodeError:
            if attempt < max_retries:
                # Retry with a slightly modified prompt
                prompt = prompt + "\n\nIMPORTANT: Your previous response was not valid JSON. Respond with ONLY a JSON object. No other text."
                continue

    return None


def _clean_json_response(text: str) -> str:
    """Strip markdown code fences and extract the JSON object."""
    # Remove markdown code blocks like ```json ... ```
    text = re.sub(r"```(?:json)?\s*", "", text)
    text = re.sub(r"```\s*", "", text)
    text = text.strip()

    # Extract everything from the first { to the last }
    start_idx = text.find('{')
    end_idx = text.rfind('}')
    
    if start_idx != -1 and end_idx != -1 and end_idx >= start_idx:
        return text[start_idx:end_idx+1]

    return text
