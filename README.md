# 🤖 CRM Voice-Bot (FastAPI + Groq)

A **Minimal CRM Automation Voice-Bot** built with **FastAPI**, powered by **Groq LLM** for natural language intent extraction, and integrated with a mock **CRM REST API**.

The bot can:

- 🧩 Create new leads
- 📅 Schedule visits
- 🔄 Update lead status

Example commands:

> “Add a new lead Rohan Sharma from Gurgaon phone 9876543210 source Instagram.”\
> “Schedule a visit for lead 12345 tomorrow at 6pm.”\
> “Update lead 12345 to FOLLOW\_UP with note sent proposal.”

---

## ✨ Features

- FastAPI-based backend for rapid deployment
- **Groq LLM API (Llama 3.1 8B)** for intent extraction
- Automatic validation for phone numbers, UUIDs, dates, and statuses
- Robust logging (`logs/crm_log.jsonl`) with timestamped API actions
- Retry handling for network/API failures
- Unit tests included for all bot actions

---

## 📂 Project Structure

```
├─ app.py                # FastAPI entry point
├─ models.py             # Pydantic models for request/response
├─ crm_client.py         # CRM API communication and logging
├─ nlu.py                # Groq-based intent and entities extraction
├─ tools.py              # tools integrated with LLM
├─ validate.py           # validate the parameters
├─ mock_crm.py           # run the server and create lead,visit schedule and update lead. (PROVIDED FILE)
├─ indext.html           # Frontend
├─ settings.py           # Configurations (CRM_BASE_URL, log file, etc.)
├─ logs/
│   └─ crm_log.jsonl     # Log file (auto-created)
├─ .env                  # Store your GROQ_API_KEY
└─ requirements.txt      # Python dependencies
```

---

## ⚡ Setup Instructions

### 1. Clone the repository

```bash
git clone https://github.com/Ritiksingh10/crm-bot.git
cd crm-bot
```

### 2. Create Environment from YAML
Create the environment from the provided `environment.yml` file:
```bash
conda env create -f environment.yml
```

### 3. Activate the Environment
```bash
conda activate capserv
```

### 4. (Optional) Verify Installed Packages
```bash
conda list
```


### 5. Configure environment variables

Create a `.env` file in the root directory:

```
GROQ_API_KEY=your_groq_api_key_here
```

---

## 🚀 Run the Application

### Terminal 1: Start Mock CRM API

```bash
uvicorn mock_crm:app --host 0.0.0.0 --port 8001 --reload
```

### Terminal 2: Start FastAPI Bot Server

```bash
python -m uvicorn app:app --host 0.0.0.0 --port 8000 --reload
```

---


## 📝 Test API Endpoints
```bash
Open the index.html file in browser and send queries.

Example:
        Add a new lead: Rohan Sharma from Gurgaon, phone 98 765 43210, source Instagram.
        Create lead name Priya Nair, city Mumbai, contact 91234-56789.
        Schedule a visit for lead 7b1b8f54 at 3 pm tomorrow
        Fix a site visit for lead 8f2a on 6 Oct 2025 at 5:00 pm IST
        Update lead 7b1b8f54 to in progress.
        Mark lead 7b1b8f54 as won. Notes: booked unit A2.
```

## 📌 Notes

- Ensure the Mock CRM API is running on port **8001** and app is running on port **8000**.
- All logs are stored in `logs/crm_log.jsonl`.
- Only **UUID or numeric IDs** are valid for lead identification.
- Supported lead statuses: `NEW`, `IN_PROGRESS`, `FOLLOW_UP`, `WON`, `LOST`.

