
import os

from typing import Annotated

from langchain.chat_models import init_chat_model
from langchain_core.tools import tool
from typing_extensions import TypedDict

from langgraph.checkpoint.memory import MemorySaver
from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import add_messages
from langgraph.prebuilt import ToolNode, tools_condition

import datetime

from langchain_core.messages import AIMessage
# from gtts import gTTS


from datetime import datetime, timedelta
import pytz


from langchain_core.messages import HumanMessage

from dotenv import load_dotenv
# Load variables from .env
load_dotenv()
# Automatically sets os.environ["GROQ_API_KEY"]
groq_key = os.getenv("GROQ_API_KEY")
os.environ["GROQ_API_KEY"] = groq_key

llm = init_chat_model("groq:llama-3.1-8b-instant")

class State(TypedDict):
    messages: Annotated[list, add_messages]

graph_builder = StateGraph(State)


# Assume timezone is always Asia/Kolkata
timezone = pytz.timezone("Asia/Kolkata")
from tools import create_lead_tool,create_visit_tool,update_lead_status_tool

  
tools = [
    create_lead_tool,
    create_visit_tool,
    update_lead_status_tool,
]


llm_with_tools = llm.bind_tools(tools)

def chatbot(state: State):
    message = llm_with_tools.invoke(state["messages"])
    # assert(len(message.tool_calls) <= 1)
    # speak(message)
    return {"messages": [message]}

graph_builder.add_node("chatbot", chatbot)

tool_node = ToolNode(tools=tools)
graph_builder.add_node("tools", tool_node)

graph_builder.add_conditional_edges(
    "chatbot",
    tools_condition,
)
graph_builder.add_edge("tools", "chatbot")
graph_builder.add_edge(START, "chatbot")

memory = MemorySaver()
graph = graph_builder.compile(checkpointer=memory)


def stream_graph_updates(user_input: str):
    print("recieved user query: ",user_input)
    config = {"configurable": {"thread_id": "1"}}

    timezone = pytz.timezone("Asia/Kolkata")
    now = datetime.now(timezone)
    weekday_name = now.strftime("%A")
    # print("TODAY'S DATE:",weekday_name)
    today_str = now.strftime("%Y-%m-%d")
    

    events = graph.stream(
        {
            "messages": [
                {"role": "system","content": f'''
You are a real-time CRM assistant.
Today's date is {today_str}, a {weekday_name}.

Your job is to:
1. Classify user input into the correct intent(s).
2. Extract all required and optional entities for each intent.
3. Call the correct tool(s) in order.
4. Use each tool’s output to form the next step or the final user response.

---------------------------------
🧰 AVAILABLE TOOLS
---------------------------------
1. create_lead_tool(name, phone, city, source=None)
2. create_visit_tool(lead_id, visit_time, notes=None)
3. update_lead_status_tool(lead_id, status, notes=None)

---------------------------------
🎯 INTENT DEFINITIONS
---------------------------------
1️⃣ LEAD_CREATE  
   • Required: name, phone, city  
   • Optional: source  

2️⃣ VISIT_SCHEDULE  
   • Required: lead_id, visit_time  
   • Optional: notes  

3️⃣ LEAD_UPDATE  
   • Required: lead_id, status  
   • Optional: notes  

4️⃣ UNKNOWN  
   • Used when the message doesn’t match any known intent.

---------------------------------
⚙️ STRICT BEHAVIOR RULES
---------------------------------
- Identify **all** intents in a single user message (can be multiple).
- Extract all required and optional entities for each intent.
- If any required or optional entity is **missing**, assign it as an **empty string ("")**.
- Always call the corresponding tool(s) with the extracted entities (even if empty).
- After each tool call:
  • If the tool’s output contains an **error**, immediately stop further processing and return that error to the user.
  • Otherwise, include the tool’s output when forming the next tool call(**only when required not necessarily**) or final response.
- Always use the **tool’s response** when generating your final reply to the user.
- **Never fabricate or reuse previous conversation data untill user give context to use it**.
- Maintain the **execution order** of intents as expressed by the user.
- If no valid intent is found, classify as UNKNOWN and respond politely without tool calls.
- **if only one intent then call tool only for that do not call any another tool after that. Just do the task that is given**.
- **if there are multiple intent and calling tool in a sequence if any tool give error message just stop there, don't call further tools. give the response with error message.

---------------------------------
🧩 EXAMPLES
---------------------------------
User: "Create a lead named Rohan from Delhi phone 9876543210"
→ Intent: LEAD_CREATE  
→ Call: create_lead_tool(name="Rohan", phone="9876543210", city="Delhi", source="")

User: "Rohit is a new lead"
→ Intent: LEAD_CREATE  
→ Call: create_lead_tool(name="Rohit", phone="", city="", source="")

User: "Schedule a visit for lead 123 tomorrow at 4 PM"
→ Intent: VISIT_SCHEDULE  
→ Call: create_visit_tool(lead_id="123", visit_time="2025-10-10T16:00:00", notes="")

User: "Create a new lead named Arjun and mark him as WON"
→ Intents: LEAD_CREATE → LEAD_UPDATE  
→ 1️⃣ create_lead_tool(name="Arjun", phone="", city="", source="")  
   → use response to get lead_id  
→ 2️⃣ update_lead_status_tool(lead_id="<lead_id_from_response>", status="WON", notes="")  

User: "Update lead 456 to WON"
→ Intent: LEAD_UPDATE  
→ Call: update_lead_status_tool(lead_id="456", status="WON", notes="")

User: "Can you help me?"
→ Intent: UNKNOWN  
→ No tool call.

---------------------------------
💬 OUTPUT FORMAT
---------------------------------
- Call tools using the exact function names and argument structure.
- Always consider tool outputs (including errors) when forming the final user message.
- If any tool output contains an "error" field, return that error message directly to the user and do not continue with further tool calls.
- **Never assume or fabricate any missing or past data untill user give context to consider pervious data**.
                '''},

                {"role": "user", "content": user_input}
            ]
        },
        config,
        stream_mode="values",
    )

    last_ai_message = None  # to store the final assistant response

    for event in events:
        if "messages" in event:
            msg = event["messages"][-1]
            # msg.pretty_print()

            # Only print & speak if it's an AI (assistant) message with actual content
            if isinstance(msg, AIMessage) and msg.content.strip():
                # msg.pretty_print()
                last_ai_message = msg.content  # store latest valid assistant response

    # After streaming ends, speak only the final assistant message (once)
    # if last_ai_message:
    #     # friendly = rephrase_for_speech(last_ai_message)
    #     # speak(friendly)
    #     print(last_ai_message)
    return last_ai_message
