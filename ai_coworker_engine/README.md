## Introduction

`ai_coworker_engine` is a small, self-contained engine for running **persona‑driven AI coworkers** (NPC‑style business agents) on top of Google Gemini.  
It is designed to be:

- **Composable**: one engine, multiple personas (CEO, CHRO, Employer Branding, etc.).
- **Stateless at the API layer**: session state is modeled explicitly and can be stored wherever you like.
- **Tool‑aware**: agents can call into Python tools (e.g. KPI calculators) as part of their reasoning loop.

The project includes:

- **Engine layer** (`engine/`): director/supervisor, LLM client, memory abstraction, agent state & safety.
- **Persona layer** (`personas/`): YAML‑defined business roles plus a registry/loader.
- **App layer** (`app/`, `streamlit_app.py`): HTTP and UI entrypoints for local testing and demos.
- **Tools layer** (`tools/`): reusable prompt snippets and domain utilities (e.g. KPI calculator).

This repo is intended as a **reference implementation** you can adapt into your own AI coworker stack.

<div align="center">
  <video src="misc/UI_preview.mp4" width="640" controls>
    Your browser does not support the video tag.  
    You can download the video directly from `misc/UI_preview.mp4`.
  </video>
</div>



---

## Quick Setup

### 1. Clone and enter the project

```bash
git clone <your-fork-or-origin> coworkerai
cd coworkerai/ai_coworker_engine
```

### 2. Create & activate a virtual environment (recommended)

On Windows (PowerShell):

```bash
#python3.11 is recommended
python -m venv .venv
.venv\Scripts\Activate.ps1
```

On macOS / Linux:

```bash
python -m venv .venv
source .venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure your Gemini API key

The engine uses Google Gemini via `google-generativeai` (see `engine/llm_client.py`).
Set the API key in your environment:

On Windows (PowerShell):

```bash
$env:GOOGLE_API_KEY = "<your_api_key_here>"
```

On macOS / Linux:

```bash
export GOOGLE_API_KEY="<your_api_key_here>"
```

You can also use a `.env` loader if you prefer; just ensure `GOOGLE_API_KEY` is available at runtime.

---

## Project Structure

High‑level layout of `ai_coworker_engine`:

```text
ai_coworker_engine/
├─ app/
│  ├─ __init__.py              # Package marker
│  ├─ api.py                   # FastAPI routes and request/response models
│  └─ main.py                  # FastAPI app creation and wiring
│
├─ engine/
│  ├─ __init__.py              # Engine package exports
│  ├─ director.py              # Director/supervisor that orchestrates personas and tools
│  ├─ llm_client.py            # GeminiLLMClient wrapper around Google Gemini API
│  ├─ memory.py                # Vector / memory abstraction (e.g. FAISS integration point)
│  ├─ npc_agent.py             # Core NPC agent logic (per‑persona behavior)
│  ├─ safety.py                # Safety, guardrails, and content‑filtering helpers
│  └─ state.py                 # Session and persona state models
│
├─ personas/
│  ├─ __init__.py              # Persona package marker
│  ├─ ceo.yaml                 # CEO persona definition (Gucci Group example)
│  ├─ chro.yaml                # CHRO persona definition
│  ├─ employer_branding.yaml   # Employer Branding / Regional persona definition
│  ├─ loader.py                # Helpers to load persona YAML files
│  └─ registry.py              # Central registry mapping persona IDs to configs
│
├─ tools/
│  ├─ kpi_calculator.py        # Example business tool callable by personas
│  └─ prompt_library.py        # Reusable prompt snippets/templates
│
│
├─ streamlit_app.py            # Streamlit UI that talks to the FastAPI backend
├─ sanity_check.py             # Simple wiring / sanity check script
├─ requirements.txt            # Python dependencies
├─ README.md                   # This file
└─ .gitignore                  # Git ignore rules for this project
```

Use this tree as a guide when navigating or extending the engine.

## Running the Engine

You have a few ways to interact with the engine locally.  
**Important:** the FastAPI service must be running before you start the Streamlit app or execute the prompt test scripts.

### 1 – Start the FastAPI service (required)

The `app/` package exposes a small FastAPI boundary you can embed in a larger system.
From the `ai_coworker_engine` directory:

```bash
uvicorn app.main:app --reload
```

Once running, you can:

- Call HTTP endpoints to create a session and send turns to the NPC.
- Integrate the engine into your own frontend or workflow tools.

> Check `app/api.py` and `app/main.py` for the exact routes and request/response models.

### 2 – Streamlit UI (optional, uses FastAPI)

`streamlit_app.py` provides a quick UI to talk to personas.  
With the FastAPI server already running in another terminal:

```bash
streamlit run streamlit_app.py
```

Then open the URL shown in your terminal (usually `http://localhost:8501`) and:

- **Select a persona** (e.g. CEO, CHRO, Employer Branding).
- **Describe a business scenario**.
- Let the **director** orchestrate the conversation and show responses.

### 3 – Local prompt tests (optional, use FastAPI)

`run_prompt_test.py` and `sanity_check.py` are simple scripts to validate prompts and wiring.  
Again, ensure the FastAPI server is running first.

Example:

```bash
python sanity_check.py
```
Use these scripts as a starting point when you add new personas, tools, or safety rules.

> **Token usage disclaimer:**  
> `run_prompt_test.py` is designed to exercise multiple prompts/personas and can consume a **large number of tokens**.  
> For reliable runs, make sure your Google Generative AI account has a **sufficient quota and relaxed token limits** (e.g. billing enabled, not on a very restricted free tier), otherwise requests may fail due to rate or usage limits.

---

## Concepts & Architecture

### Design Highlights

- **Persona‑driven AI engineering**
  - Persona definitions in `personas/*.yaml` with business‑level context.
  - Session‑scoped NPC state (conversations are modeled explicitly, not hidden in the LLM).
  - Tool‑aware responses via functions under `tools/`.

- **AI Ops & scalability**
  - FastAPI boundary in `app/` for clean integration with other services.
  - Pluggable LLM providers via `engine/llm_client.py` (Gemini by default, but can be swapped).
  - Vector/memory abstraction in `engine/memory.py` (e.g. FAISS or other stores).

- **System design**
  - `engine/director.py` acts as a **supervisor**: controls pacing, decides when/which persona/tool to call.
  - `engine/state.py` keeps persona, context, and safety‑related flags decoupled from transport.
  - One engine instance can support **multiple NPC roles** in parallel sessions.

---

## Extending the Engine

### Add a new persona

1. **Create a YAML file** under `personas/` (e.g. `sales_director.yaml`) defining:
   - High‑level role description
   - Goals and guardrails
   - Tone and communication style
2. **Register the persona** in `personas/registry.py`.
3. **(Optional) Add prompts** in `tools/prompt_library.py` for reusable question templates.
4. **(Optional) Add tools** in `tools/` and wire them into the director/agent logic.

Restart the app (Streamlit or FastAPI) and you should see/use the new persona.

### Swap or configure the LLM

The default LLM client is `GeminiLLMClient` in `engine/llm_client.py`. To customize:

- Change the `model` name (e.g. `"gemini-2.5-pro"`).
- Adjust `max_output_tokens`, `max_prompt_chars`, or `temperature`.
- Or implement a new client with the same `generate(prompt: str) -> str` interface and wire it into your app layer.

---

## Manual: Typical Development Workflow

1. **Set up** the environment and API key (see *Quick Setup*).
2. **Start** the FastAPI server (see *Running the Engine*).
3. **Optionally run** the Streamlit app and/or prompt test scripts against that server.
4. **Iterate on prompts**:
   - Update persona YAMLs.
   - Refine snippets in `tools/prompt_library.py`.
   - Re‑run `sanity_check.py` or your own tests.
5. **Instrument & harden**:
   - Add safety checks in `engine/safety.py`.
   - Add logging or tracing around director decisions.
6. **Integrate**:
   - Wrap FastAPI endpoints into your product frontend.
   - Or embed the engine as a Python library in your own backend.

This gives you a clear path from **local experimentation** to a **production‑ready AI coworker**.