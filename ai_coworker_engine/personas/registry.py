from personas.loader import load_persona

AVAILABLE_PERSONAS = {
    "chro": "chro",
    "ceo": "ceo",
    "employer_branding": "employer_branding"
}

def get_persona(persona_key: str) -> dict:
    if persona_key not in AVAILABLE_PERSONAS:
        raise ValueError(f"Invalid persona key: {persona_key}")

    return load_persona(AVAILABLE_PERSONAS[persona_key])