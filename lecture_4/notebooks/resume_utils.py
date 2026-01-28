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


def load_job_requirements(file_path: str) -> str:
    """
    Load job requirements from a markdown file.

    Args:
        file_path: Path to the job requirements file

    Returns:
        String containing the job requirements
    """
    with open(file_path, 'r', encoding='utf-8') as f:
        return f.read()


def structured_llm_call(
    api_key: str,
    prompt: str,
    context_data: Dict[str, Any],
    output_schema: Dict[str, Any],
    model: str = "anthropic/claude-3.5-sonnet",
    temperature: float = 0.2
) -> Dict[str, Any]:
    """
    Generic function for making structured LLM calls with OpenRouter.

    This function handles:
    - Building the full prompt with context
    - Making the API call
    - Parsing the JSON response
    - Error handling

    Args:
        api_key: OpenRouter API key
        prompt: The instruction/task description
        context_data: Dictionary of context (e.g., {'resume': '...', 'job_req': '...'})
        output_schema: Dictionary describing the expected JSON structure
        model: Model to use (default: Claude 3.5 Sonnet)
        temperature: Sampling temperature (0.0-1.0, lower = more consistent)

    Returns:
        Dict with:
            - 'result': Parsed JSON output (or None if error)
            - 'error': Error message (or None if successful)
            - 'usage': Token usage statistics

    Example:
        >>> result = structured_llm_call(
        ...     api_key="sk-...",
        ...     prompt="Extract years of experience from this resume.",
        ...     context_data={'resume': resume_text},
        ...     output_schema={
        ...         'years_experience': 'number',
        ...         'evidence': ['list of quotes from resume']
        ...     }
        ... )
        >>> print(result['result']['years_experience'])
        5
    """
    # Build context section
    context_str = ""
    for key, value in context_data.items():
        # Truncate long text fields to avoid token limits
        if isinstance(value, str) and len(value) > 5000:
            value = value[:5000] + "\n... (truncated)"
        context_str += f"\n{key.upper()}:\n{value}\n"

    # Build schema description
    schema_str = json.dumps(output_schema, indent=2)

    # Construct full prompt
    full_prompt = f"""{prompt}

{context_str}

Return a JSON object with this exact structure:
{schema_str}

IMPORTANT: Return ONLY valid JSON, no additional text or markdown formatting."""

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
        "max_tokens": 2000,
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
