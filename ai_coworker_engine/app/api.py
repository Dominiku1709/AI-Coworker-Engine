# app/api.py
import os
from dotenv import load_dotenv
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from personas.registry import get_persona
from engine.npc_agent import NPCAgent
from engine.state import NPCState
from engine.llm_client import GeminiLLMClient

router = APIRouter()

# --------------------------------------------------
# In-memory session store (prototype only)
# --------------------------------------------------

AGENTS = {}

load_dotenv()
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
if not GEMINI_API_KEY:
    raise RuntimeError(
        "GEMINI_API_KEY is not set. Add it to your environment or your .env file."
    )

llm = GeminiLLMClient(api_key=os.getenv("GEMINI_API_KEY"))  # API key read from env


# --------------------------------------------------
# Request / Response Models
# --------------------------------------------------

class ChatRequest(BaseModel):
    persona_id: str
    message: str


class ChatResponse(BaseModel):
    persona: str
    response: str
    state: dict


# --------------------------------------------------
# Chat Endpoint
# --------------------------------------------------

@router.post("/chat", response_model=ChatResponse)
def chat(req: ChatRequest):
    persona_id = req.persona_id

    # Load or reuse agent
    if persona_id not in AGENTS:
        try:
            persona = get_persona(persona_id)
        except KeyError:
            raise HTTPException(status_code=404, detail="Persona not found")

        agent = NPCAgent(
            persona=persona,
            llm_client=llm,
            tools=persona.get("allowed_tools", [])
        )
        agent.initialize_state(NPCState())
        AGENTS[persona_id] = agent

    agent = AGENTS[persona_id]

    response, state = agent.respond(req.message)

    return ChatResponse(
        persona=agent.persona["role"],
        response=response,
        state={
            "relationship_score": state.relationship_score,
            "frustration_level": state.frustration_level,
            "is_blocked": state.is_blocked
        }
    )