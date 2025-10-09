from langchain.tools import tool

# from langchain.tools import tool
from crm_client import create_lead, schedule_visit, update_lead
from validate import validate_city,validate_datetime,validate_lead_id,validate_name,validate_phone,validate_status

# ---------------------------------------------------------------------------
# 🧰 Tool 1: Create Lead
# ---------------------------------------------------------------------------
@tool
def create_lead_tool(name: str, phone: str, city: str, source: str = None):
    """
    Create a new lead in the CRM system.

    Args:
        name: Name of the lead.
        phone: Phone number of the lead.
        city: City where the lead is located.
        source: Optional source (e.g., 'website', 'referral').

    Returns:
        dict: Response from the CRM API or error details.
    """
    payload = {
        "name": name,
        "phone": phone,
        "city": city,
        "source": source,
    }

    # Validate mandatory fields
    validation_errors = []
    for field in ["name", "phone", "city"]:
        if not payload.get(field):
            validation_errors.append(f"Missing required field: {field}")
    
    if(validate_phone(phone)==None):
        validation_errors.append("Invalid phone number")
    if(validate_name(name)==None):
        validation_errors.append("Invalid name")
    if(validate_city(city)==None):
        validation_errors.append("Invalid city")


    return create_lead(payload, validation_errors)


# ---------------------------------------------------------------------------
# 🧰 Tool 2: Schedule Visit
# ---------------------------------------------------------------------------
@tool
def create_visit_tool(lead_id: str, visit_time: str, notes: str = None):
    """
    Schedule a visit for a given lead.

    Args:
        lead_id: The unique ID of the lead.
        visit_time: Date and time of the visit (ISO 8601 format).
        notes: Optional notes for the visit.

    Returns:
        dict: Response from the CRM API or error details.
    """
    payload = {
        "lead_id": lead_id,
        "visit_time": visit_time,
        "notes": notes,
    }

    validation_errors = []
    if not lead_id:
        validation_errors.append("Lead ID is required.")
    else:
        if(validate_lead_id(lead_id)==None):
            validation_errors.append("Invalid lead_id, it should be valid uuid")
    
    if not visit_time:
        validation_errors.append("Visit time is required.")
    else:
        if(validate_datetime(visit_time)==None):
            validation_errors.append("Invalid time/LLM does not able to parse it correctly")

    return schedule_visit(payload, validation_errors)


# ---------------------------------------------------------------------------
# 🧰 Tool 3: Update Lead Status
# ---------------------------------------------------------------------------
@tool
def update_lead_status_tool(lead_id: str, status: str, notes: str = None):
    """
    Update the status of an existing lead.

    Args:
        lead_id: The unique ID of the lead.
        status: New lead status (must be one of: NEW, IN_PROGRESS, FOLLOW_UP, WON, LOST).
        notes: Optional notes for this update.

    Returns:
        dict: Response from the CRM API or error details.
    """
    payload = {
        "status": status,
        "notes": notes,
    }

    validation_errors = []
    allowed_statuses = ["NEW", "IN_PROGRESS", "FOLLOW_UP", "WON", "LOST"]

    if not lead_id:
        validation_errors.append("Lead ID is required.")   
    else:
        if(validate_lead_id(lead_id)==None):
            validation_errors.append("Invalid lead_id, it should be valid uuid")

    if not status:
        validation_errors.append(f"Status is required. Must be one of {allowed_statuses}")
    else:
        if(validate_status(status)==None):
            validation_errors.append(f"Invalid status '{status}'. Must be one of {allowed_statuses}")

    return update_lead(payload, lead_id, validation_errors)

