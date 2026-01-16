"""Utility functions for resume screening with LLMs."""

from typing import Any, Dict
import httpx
import json
import csv


def load_resumes(csv_path: str) -> Dict[str, Dict[str, str]]:
    """
    Load all resumes from CSV into a dictionary.

    Args:
        csv_path: Path to the resumes CSV file

    Returns:
        Dict mapping resume ID to resume data (ID, Resume_str, Resume_html)
    """
    resumes = {}
    with open(csv_path, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            resumes[row['ID']] = {
                'ID': row['ID'],
                'Resume_str': row['Resume_str'],
                'Resume_html': row['Resume_html']
            }
    return resumes


def analyze_resume(
    api_key: str,
    prompt: str,
    resume_text: str,
    output_schema: str,
    model: str = "anthropic/claude-3.5-sonnet",
    temperature: float = 0.3
) -> Dict[str, Any]:
    """
    Analyze a resume using an LLM with structured output.

    Args:
        api_key: OpenRouter API key
        prompt: The instruction for what to analyze
        resume_text: The resume text to analyze
        output_schema: JSON schema description for the output format
        model: Model to use (default: Claude 3.5 Sonnet)
        temperature: Sampling temperature (default: 0.3 for consistency)

    Returns:
        Dict with 'result' (parsed JSON), 'error' (if any), and 'usage' (token counts)
    """
    # Build the full prompt
    full_prompt = f"""{prompt}

Resume:
{resume_text[:3000]}

Return a JSON object with this structure:
{output_schema}

Return ONLY valid JSON, no additional text."""

    # Make API call
    url = "https://openrouter.ai/api/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
    }
    payload = {
        "model": model,
        "messages": [{"role": "user", "content": full_prompt}],
        "temperature": temperature,
        "max_tokens": 1500,
        "response_format": {"type": "json_object"}
    }

    try:
        with httpx.Client(timeout=60) as client:
            resp = client.post(url, headers=headers, json=payload)
            resp.raise_for_status()
            data = resp.json()

            content = data["choices"][0]["message"]["content"]
            result = json.loads(content)

            return {
                "result": result,
                "error": None,
                "usage": data.get("usage", {})
            }
    except Exception as e:
        return {
            "result": None,
            "error": str(e),
            "usage": {}
        }
