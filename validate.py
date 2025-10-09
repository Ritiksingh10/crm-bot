
import re
import uuid
from dateutil import parser

def validate_lead_id(lead_id: str) -> str | None:
    """
    Validate a lead ID (UUID or numeric).

    Parameters
    ----------
    lead_id : str
        The lead ID to validate.

    Returns
    -------
    str | None
        The valid lead_id or None if invalid.
    """
    
    try:
        uuid.UUID(lead_id)
        return lead_id
    except ValueError:
        if str(lead_id).isdigit():
            return lead_id
    return None

def validate_phone(phone: str) -> str | None:
    """
    Validate an Indian phone number.

    Parameters
    ----------
    phone : str
        The phone number to validate.

    Returns
    -------
    str | None
        A cleaned, valid phone number if valid, otherwise None.
    """
    
    match = re.match(r"(\+91[-\s]?)?[6-9]\d{9}$", phone.replace(" ", "").replace("-", ""))
    return match.group() if match else None
    

def validate_datetime(dt_str: str) -> str | None:
    """
    Validate and convert date/time strings to ISO 8601 format.

    Parameters
    ----------
    dt_str : str
        The datetime string to validate (e.g., 'tomorrow 6pm').

    Returns
    -------
    str | None
        ISO 8601 formatted datetime or None if invalid.
    """
    
    try:
        return parser.parse(dt_str).isoformat()
    except Exception:
        return None



def validate_name(name: str) -> str | None:
    """
    Validates a person's name.
    
    Rules:
    - Must be a non-empty string.
    - Only letters, spaces, hyphens, and apostrophes allowed.
    - Strips leading/trailing spaces.
    
    Returns:
    - Validated name as string.
    - None if invalid or empty.
    """
    
    cleaned = name.strip()
    if re.match(r"^[A-Za-z\s\-\']+$", cleaned):
        return cleaned
    return None

def validate_city(city: str) -> str | None:
    """
    Validates a city name.
    
    Rules:
    - Must be a non-empty string.
    - Only letters, spaces, and hyphens allowed.
    - Strips leading/trailing spaces.
    
    Returns:
    - Validated city as string.
    - None if invalid or empty.
    """
    
    cleaned = city.strip()
    if re.match(r"^[A-Za-z\s\-]+$", cleaned):
        return cleaned
    return None
def validate_status(status: str) -> str | None:
    """
    Validate lead status.

    Parameters
    ----------
    status : str
        Status string (e.g., 'FOLLOW_UP', 'NEW').

    Returns
    -------
    str | None
        Uppercase valid status or None if not in allowed set.
    """

    # Allowed status values for lead updates
    ALLOWED_STATUS = {"NEW", "IN_PROGRESS", "FOLLOW_UP", "WON", "LOST"}

    
    return status.upper() if status.upper() in ALLOWED_STATUS else None
