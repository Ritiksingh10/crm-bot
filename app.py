"""
app.py
-------
Main FastAPI application file for the Minimal CRM Bot.

This service provides a REST API endpoint that processes chatbot requests,
extracts intents and entities using an NLU module, and performs appropriate
CRM operations (like creating leads, updating leads, or scheduling visits)
based on the extracted intent.

Modules Used:
- FastAPI: For creating and running the web service.
- models: Defines data models for request and response validation.
- nlu: Handles intent and entity extraction from user transcripts.
- crm_client: Contains functions to interact with the CRM system (mock or real).

"""

from fastapi import FastAPI
from models import BotRequest, BotResponse
from nlu import stream_graph_updates



from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="Minimal CRM Bot")

# Allow your frontend to access the backend
origins = [
    "http://localhost:5500",  # if using Live Server / local HTML
    "http://127.0.0.1:5500",
    "http://localhost:3000",  # optional: React, etc.
    "http://127.0.0.1:3000",
    "*",  # ⚠️ for testing only, allows all origins
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],  # allow GET, POST, OPTIONS, etc.
    allow_headers=["*"],  # allow all headers
)




# # Initialize FastAPI app
# app = FastAPI(title="Minimal CRM Bot")

@app.post("/bot/handle")
def handle_bot(request: BotRequest):
    """
    Endpoint to handle chatbot requests and perform corresponding CRM actions.

    Parameters
    ----------
    request : BotRequest
        The input request body containing the user's transcript (text message).

    Returns
    -------
    BotResponse
        JSON response containing the status ("success") and the results of each
        identified intent (e.g., lead creation, visit scheduling, etc.).

    Flow
    ----
    1. Extract the transcript text from the request.
    2. Pass the transcript to the NLU module to extract intents and entities.
    3. For each detected intent:
        - Identify required and optional entities.
        - Route the request to the appropriate CRM client function.
    4. Aggregate all results and return a structured response.
    """

    # Step 1: Extract transcript text
    transcript = request.transcript

    # Step 2: Extract intents and entities using NLU module
    nlu_output = stream_graph_updates(transcript)
    print("nlu_output: ",nlu_output)
    # return nlu_output
    return {"answer": nlu_output}  # simple dict with string
