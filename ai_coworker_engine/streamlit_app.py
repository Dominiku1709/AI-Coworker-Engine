import streamlit as st
import requests
import time

API_URL = "http://localhost:8000/chat"

# -------------------------------------------------
# Persona Configuration (STRICT SEPARATION)
# -------------------------------------------------

PERSONAS = {
    "ceo": {
        "label": "CEO",
        "avatar": "💼",
        "description": (
            "Strategic, long-term, group-level perspective. "
            "Prioritizes brand equity and alignment over short-term efficiency."
        ),
    },
    "chro": {
        "label": "CHRO",
        "avatar": "👥",
        "description": (
            "People, culture, and organizational health. "
            "Focuses on talent, capability building, and sustainability."
        ),
    },
    "employer_branding": {
        "label": "Employer Branding",
        "avatar": "🎨",
        "description": (
            "External perception, storytelling, and talent attraction. "
            "Balances authenticity with positioning."
        ),
    },
}

# -------------------------------------------------
# Page Setup
# -------------------------------------------------

st.set_page_config(
    page_title="AI Co-worker Simulator",
    layout="centered",
)

# -------------------------------------------------
# Sidebar — Persona Selector
# -------------------------------------------------

st.sidebar.title("AI Co-worker")

persona_ids = list(PERSONAS.keys())
persona_labels = [
    f"{PERSONAS[p]['avatar']} {PERSONAS[p]['label']}"
    for p in persona_ids
]

selected_label = st.sidebar.radio(
    "Choose role",
    persona_labels,
)

selected_persona_id = persona_ids[
    persona_labels.index(selected_label)
]

# -------------------------------------------------
# Session State (Authoritative)
# -------------------------------------------------

if "active_persona" not in st.session_state:
    st.session_state.active_persona = selected_persona_id

if "messages" not in st.session_state:
    st.session_state.messages = []

persona_changed = (
    st.session_state.active_persona != selected_persona_id
)

if persona_changed:
    st.session_state.active_persona = selected_persona_id
    st.session_state.messages = []

# -------------------------------------------------
# Resolve Persona (FROM STATE ONLY)
# -------------------------------------------------

persona = PERSONAS[st.session_state.active_persona]

# -------------------------------------------------
# Sidebar — Active Role Context
# -------------------------------------------------

st.sidebar.divider()
st.sidebar.subheader("Active Role")
st.sidebar.markdown(
    f"**{persona['avatar']} {persona['label']}**"
)
st.sidebar.caption(persona["description"])

# -------------------------------------------------
# Main Header
# -------------------------------------------------

st.markdown(
    f"## {persona['avatar']} {persona['label']}"
)
st.caption(persona["description"])

if persona_changed:
    st.divider()
    st.caption("New role selected — context reset.")

# -------------------------------------------------
# Chat History (CORRECT AVATAR PER MESSAGE)
# -------------------------------------------------

for msg in st.session_state.messages:
    with st.chat_message(
        msg["role"],
        avatar=msg.get("avatar"),
    ):
        st.markdown(msg["content"])

# -------------------------------------------------
# Chat Input & Backend Call
# -------------------------------------------------

user_input = st.chat_input("Type your message")

if user_input:
    # ---- USER MESSAGE ----
    with st.chat_message("user"):
        st.markdown(user_input)

    st.session_state.messages.append(
        {
            "role": "user",
            "content": user_input,
            "avatar": None,
        }
    )

    # ---- ASSISTANT MESSAGE ----
    with st.chat_message(
        "assistant",
        avatar=persona["avatar"],
    ):
        placeholder = st.empty()

        try:
            resp = requests.post(
                API_URL,
                json={
                    "persona_id": st.session_state.active_persona,
                    "message": user_input,
                },
                timeout=60,
            )
            resp.raise_for_status()

            assistant_text = resp.json().get(
                "response", "[No response]"
            )

        except requests.exceptions.Timeout:
            assistant_text = "Request timed out. Please try again."

        except requests.exceptions.RequestException as e:
            assistant_text = f"Backend error: {e}"

        # ---- Typing Effect ----
        rendered = ""
        for word in assistant_text.split(" "):
            rendered += word + " "
            placeholder.markdown(rendered)
            time.sleep(0.03)

    # ---- Persist AFTER render ----
    st.session_state.messages.append(
        {
            "role": "assistant",
            "content": assistant_text,
            "avatar": persona["avatar"],
        }
    )