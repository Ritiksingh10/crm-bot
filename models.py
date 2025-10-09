"""
models.py
----------
This module defines all Pydantic models used for validating and structuring
requests and responses in the Minimal CRM Bot API.

Pydantic provides type validation and automatic JSON serialization/deserialization
for FastAPI, ensuring that data sent and received through API endpoints
is clean, well-defined, and consistent.

Classes:
- BotRequest: Defines the input structure for chatbot queries.
- IntentResult: Defines how each detected intent and its outcome are represented.
- BotResponse: Defines the complete API response returned by the bot handler.

"""

from pydantic import BaseModel
from typing import Any, Dict, List

# ---------------------------------------------------------------------------
# BotRequest
# ---------------------------------------------------------------------------
class BotRequest(BaseModel):
    """
    Represents the input structure sent to the chatbot API.

    Attributes
    ----------
    transcript : str
        The raw text or speech transcript provided by the user.
    
    Example
    -------
    {
        "transcript": "Add a new lead Rohan Sharma from Gurgaon phone 9876543210 source Instagram."
    }
    """
    transcript: str


# ---------------------------------------------------------------------------
# IntentResult
# ---------------------------------------------------------------------------
class IntentResult(BaseModel):
    """
    Represents the outcome of processing a single detected intent
    from the user’s input (e.g., lead creation, lead update, visit scheduling).

    Attributes
    ----------
    intent : str
        The name of the detected intent (e.g., "LEAD_CREATE").
    result : Dict[str, Any] | None
        The data returned from the CRM API for the given intent.
    error : str | None
        Error message if the operation failed.

    Example
    -------
    {
        "intent": "LEAD_CREATE",
        "result": {"lead_id": "b77e52a1-30c3-4d7f-9378-af5dfdb8dbde"},
        "error": null
    }
    """
    intent: str
    result: Dict[str, Any] | None = None
    error: str | None = None


# ---------------------------------------------------------------------------
# BotResponse
# ---------------------------------------------------------------------------
class BotResponse(BaseModel):
    """
    Represents the full API response returned by the chatbot
    after handling the user’s input.

    Attributes
    ----------
    status : str
        Overall request status (e.g., "success" or "failure").
    result : List[IntentResult]
        A list of all processed intents and their respective results.

    Example
    -------
    {
        "status": "success",
        "result": [
            {
                "intent": "LEAD_CREATE",
                "result": {"lead_id": "b77e52a1-30c3-4d7f-9378-af5dfdb8dbde"},
                "error": null
            }
        ]
    }
    """
    status: str
    result: List[IntentResult]
