"""Utility functions for building a simple application routing agent."""

from typing import Any, Dict, List
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
    """Load job requirements from a markdown file."""
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

    Args:
        api_key: OpenRouter API key
        prompt: The instruction/task description
        context_data: Dictionary of context (e.g., {'resume': '...', 'job_req': '...'})
        output_schema: Dictionary describing the expected JSON structure
        model: Model to use
        temperature: Sampling temperature

    Returns:
        Dict with 'result', 'error', and 'usage'
    """
    # Build context section
    context_str = ""
    for key, value in context_data.items():
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


# ============================================================================
# TOOLS - Python functions that the agent can call
# ============================================================================

def schedule_technical_assessment(candidate_id: str, assessment_type: str) -> Dict[str, Any]:
    """
    Schedule a technical assessment for a candidate.

    Args:
        candidate_id: The candidate's ID
        assessment_type: Type of assessment (e.g., 'coding_challenge', 'system_design')

    Returns:
        Dict with status and scheduled date
    """
    return {
        "status": "success",
        "message": f"Technical assessment ({assessment_type}) scheduled for candidate {candidate_id}",
        "assessment_type": assessment_type,
        "scheduled_date": "2024-02-15"  # Mock date
    }


def route_to_department(candidate_id: str, department: str, reason: str) -> Dict[str, Any]:
    """
    Route candidate to a specific department/hiring manager.

    Args:
        candidate_id: The candidate's ID
        department: Department to route to
        reason: Reason for routing

    Returns:
        Dict with status and routing info
    """
    return {
        "status": "success",
        "message": f"Candidate {candidate_id} routed to {department}",
        "department": department,
        "reason": reason
    }


def request_additional_info(candidate_id: str, info_needed: str) -> Dict[str, Any]:
    """
    Request additional information from candidate.

    Args:
        candidate_id: The candidate's ID
        info_needed: Description of what information is needed

    Returns:
        Dict with status and request details
    """
    return {
        "status": "success",
        "message": f"Additional info requested from candidate {candidate_id}",
        "info_needed": info_needed,
        "request_sent_date": "2024-02-01"  # Mock date
    }


def reject_application(candidate_id: str, reason: str) -> Dict[str, Any]:
    """
    Reject a candidate's application.

    Args:
        candidate_id: The candidate's ID
        reason: Reason for rejection

    Returns:
        Dict with status and rejection details
    """
    return {
        "status": "success",
        "message": f"Application rejected for candidate {candidate_id}",
        "reason": reason,
        "rejection_email_sent": True
    }


def flag_for_manual_review(candidate_id: str, concern: str) -> Dict[str, Any]:
    """
    Flag candidate for manual human review.

    Args:
        candidate_id: The candidate's ID
        concern: Description of the concern requiring review

    Returns:
        Dict with status and flag details
    """
    return {
        "status": "success",
        "message": f"Candidate {candidate_id} flagged for manual review",
        "concern": concern,
        "assigned_to": "hiring_manager"  # Mock assignment
    }


def send_email(candidate_id: str, template: str) -> Dict[str, Any]:
    """
    Send an email to the candidate.

    Args:
        candidate_id: The candidate's ID
        template: Email template to use

    Returns:
        Dict with status and email details
    """
    return {
        "status": "success",
        "message": f"Email sent to candidate {candidate_id}",
        "template": template,
        "sent_date": "2024-02-01"  # Mock date
    }


def done(candidate_id: str) -> Dict[str, Any]:
    """
    Signal that the agent is done processing this candidate.

    Args:
        candidate_id: The candidate's ID

    Returns:
        Dict with completion status
    """
    return {
        "status": "success",
        "message": f"Processing complete for candidate {candidate_id}",
        "final": True
    }


# ============================================================================
# TOOL REGISTRY - Describes available tools for the agent
# ============================================================================

TOOL_REGISTRY = {
    "schedule_technical_assessment": {
        "function": schedule_technical_assessment,
        "description": "Schedule a technical assessment (coding challenge, system design, etc.) for a promising candidate",
        "parameters": {
            "candidate_id": "string - The candidate's ID",
            "assessment_type": "string - Type of assessment: 'coding_challenge', 'system_design', 'live_coding'"
        }
    },
    "route_to_department": {
        "function": route_to_department,
        "description": "Route candidate to a specific department or hiring manager for further review",
        "parameters": {
            "candidate_id": "string - The candidate's ID",
            "department": "string - Department name: 'senior_engineering', 'junior_engineering', 'internship'",
            "reason": "string - Reason for routing to this department"
        }
    },
    "request_additional_info": {
        "function": request_additional_info,
        "description": "Request additional information from the candidate (e.g., missing education details, clarification)",
        "parameters": {
            "candidate_id": "string - The candidate's ID",
            "info_needed": "string - Description of what information is needed"
        }
    },
    "reject_application": {
        "function": reject_application,
        "description": "Reject the candidate's application with a reason",
        "parameters": {
            "candidate_id": "string - The candidate's ID",
            "reason": "string - Reason for rejection (be professional and constructive)"
        }
    },
    "flag_for_manual_review": {
        "function": flag_for_manual_review,
        "description": "Flag candidate for manual human review when uncertain or edge case",
        "parameters": {
            "candidate_id": "string - The candidate's ID",
            "concern": "string - Description of what requires human judgment"
        }
    },
    "send_email": {
        "function": send_email,
        "description": "Send an email to the candidate using a template",
        "parameters": {
            "candidate_id": "string - The candidate's ID",
            "template": "string - Template name: 'technical_interview_invite', 'rejection', 'request_info'"
        }
    },
    "done": {
        "function": done,
        "description": "Signal that processing is complete for this candidate. Call this when no further automated actions are needed.",
        "parameters": {
            "candidate_id": "string - The candidate's ID"
        }
    }
}
