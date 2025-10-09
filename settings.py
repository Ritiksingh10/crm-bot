"""
settings.py
------------
This module defines configuration constants for the CRM Bot application.
These constants are used across different modules to maintain consistent
URLs, logging configuration, and retry strategies.
"""

# ----------------------------
# CRM Service Configuration
# ----------------------------

# Base URL of the CRM microservice (used for lead creation, updates, etc.)
CRM_BASE_URL = "http://127.0.0.1:8001/crm"

# ----------------------------
# Logging Configuration
# ----------------------------

# File path for application logs.
# The `.jsonl` (JSON Lines) format allows easy log parsing and streaming.
LOG_FILE = "logs/crm_log.jsonl"

# ----------------------------
# Retry Settings
# ----------------------------

# Number of times to retry an API call if it fails due to a network issue or server error.
RETRIES = 2

# Delay (in seconds) before retrying a failed request.
BACKOFF = 1