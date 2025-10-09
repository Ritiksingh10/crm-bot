"""
crm_client.py
--------------
This module handles all interactions with the CRM system (mock or real) and logs
each action performed by the chatbot.

Features:
- API calls for creating leads, scheduling visits, and updating lead statuses.
- Automatic retry mechanism for transient network failures.
- Centralized logging of all API actions in JSON Lines format for traceability.

Modules Used:
- requests: For sending HTTP requests to the CRM API.
- os, json, datetime: For file handling, serialization, and timestamping.
- settings: Contains configuration constants like CRM_BASE_URL, RETRIES, and BACKOFF.

"""

import os
import requests
from requests.adapters import HTTPAdapter, Retry
from settings import CRM_BASE_URL, RETRIES, BACKOFF
from datetime import datetime
import json

# Path to store all CRM interaction logs
LOG_FILE = "logs/crm_log.jsonl"

# ✅ Ensure the 'logs' directory exists before writing log files
os.makedirs("logs", exist_ok=True)

# ---------------------------------------------------------------------------
# HTTP Session Setup with Retry Mechanism
# ---------------------------------------------------------------------------
# The Retry strategy helps handle temporary failures (e.g., 502, 503) by
# automatically retrying the request before throwing an error.
session = requests.Session()
retries = Retry(
    total=RETRIES,
    backoff_factor=BACKOFF,
    status_forcelist=[500, 502, 503, 504],
)
session.mount("http://", HTTPAdapter(max_retries=retries))
session.mount("https://", HTTPAdapter(max_retries=retries))

# ---------------------------------------------------------------------------
# Helper Function: Logging CRM Actions
# ---------------------------------------------------------------------------
def log_action(action: str, entities: dict, success: bool, output: dict = None, error: str = None):
    """
    Logs every CRM-related action (lead creation, visit scheduling, etc.) to a file.

    Parameters
    ----------
    action : str
        The type of CRM action performed (e.g., "LEAD_CREATE").
    entities : dict
        The payload or data involved in the action.
    success : bool
        Indicates whether the action succeeded (True) or failed (False).
    output : dict, optional
        The response data returned by the CRM API.
    error : str, optional
        The error message (if the request failed).

    Log Format
    -----------
    Each log entry is stored as a JSON object on a new line in `logs/crm_log.jsonl`.
    Example:
    {
        "timestamp": "2025-10-05T21:00:00",
        "action": "LEAD_CREATE",
        "entities": {"name": "Rohan Sharma", "phone": "9876543210"},
        "success": true,
        "output": {"lead_id": "b77e52a1-30c3-4d7f-9378-af5dfdb8dbde"},
        "error": null
    }
    """
    entry = {
        "timestamp": datetime.now().isoformat(),
        "action": action,
        "entities": entities,
        "success": success,
        "output": output,
        "error": error,
    }

    # Append each log entry as a single line of JSON
    with open(LOG_FILE, "a") as f:
        f.write(json.dumps(entry) + "\n")

    # # Print summary in console for quick debugging
    # print(f"[{entry['timestamp']}] {action} | success={success}")


# ---------------------------------------------------------------------------
# CRM Operation: Create Lead
# ---------------------------------------------------------------------------
def create_lead(payload: dict, validation_errors: list = None) -> dict:
    validation_errors = validation_errors or []
    """
    Create a new lead in the CRM system.

    Parameters
    ----------
    payload : dict
        Dictionary containing lead details (e.g., name, phone, city, source).

    Returns
    -------
    dict
        JSON response from the CRM API or error details in case of failure.
    """
    if validation_errors:
        error_message = "Validation errors: " + str(validation_errors)
        log_action("LEAD_CREATE", payload, False, error=error_message)
        return {"error": error_message}
    try:
        res = session.post(f"{CRM_BASE_URL}/leads", json=payload, timeout=5)
        res.raise_for_status()
        data = res.json()
        log_action("LEAD_CREATE", payload, True, output=data)
        return data
    except Exception as e:
        # Combine HTTP/API error with validation errors
        error_message = str(e)
        log_action("LEAD_CREATE", payload, False, error=error_message)
        return {"error": error_message}

# ---------------------------------------------------------------------------
# CRM Operation: Schedule Visit
# ---------------------------------------------------------------------------
# def schedule_visit(payload: dict) -> dict:
def schedule_visit(payload: dict, validation_errors: list = None) -> dict:
    validation_errors = validation_errors or []
    """
    Schedule a visit for an existing lead in the CRM system.

    Parameters
    ----------
    payload : dict
        Dictionary containing visit details (e.g., lead_id, date_time, notes).

    Returns
    -------
    dict
        JSON response from the CRM API or error details in case of failure.
    """
    if validation_errors:
        error_message = "Validation errors: " + str(validation_errors)
        log_action("VISIT_SCHEDULE", payload, False, error=error_message)
        return {"error": error_message}
    try:
        res = session.post(f"{CRM_BASE_URL}/visits", json=payload, timeout=5)
        res.raise_for_status()
        data = res.json()
        log_action("VISIT_SCHEDULE", payload, True, output=data)
        return data
    except requests.exceptions.HTTPError as e:
        error_message = str(e)
        try:
            # Try to extract JSON error message from server
            detail = res.json().get("detail", "")
            if detail:
                error_message += f" | Detail: {detail}"
        except Exception:
            pass
        log_action("VISIT_SCHEDULE", payload, False, error=error_message)
        return {"error": error_message}
    except Exception as e:
        # For any other errors
        error_message = str(e)
        log_action("VISIT_SCHEDULE", payload, False, error=error_message)
        return {"error": error_message}


# ---------------------------------------------------------------------------
# CRM Operation: Update Lead
# ---------------------------------------------------------------------------
# def update_lead(payload: dict, lead_id: str) -> dict:
def update_lead(payload: dict, lead_id: str, validation_errors: list = None) -> dict:
    validation_errors = validation_errors or []
    """
    Update the status or details of an existing lead in the CRM system.

    Parameters
    ----------
    payload : dict
        Dictionary containing updated information (e.g., status, notes).
    lead_id : str
        Unique identifier of the lead to be updated.

    Returns
    -------
    dict
        JSON response from the CRM API or error details in case of failure.
    """
    if validation_errors:
        error_message = "Validation errors: " + str(validation_errors)
        log_action("LEAD_UPDATE", payload, False, error=error_message)
        return {"error": error_message}
    try:
        res = session.post(f"{CRM_BASE_URL}/leads/{lead_id}/status", json=payload, timeout=5)
        res.raise_for_status()
        data = res.json()
        log_action("LEAD_UPDATE", payload, True, output=data)
        return data
    except requests.exceptions.HTTPError as e:
        error_message = str(e)
        try:
            # Try to extract JSON error message from server
            detail = res.json().get("detail", "")
            if detail:
                error_message += f" | Detail: {detail}"
        except Exception:
            pass
        log_action("LEAD_UPDATE", payload, False, error=error_message)
        return {"error": error_message}
    except Exception as e:
        # For any other errors
        error_message = str(e)
        log_action("LEAD_UPDATE", payload, False, error=error_message)
        return {"error": error_message}
