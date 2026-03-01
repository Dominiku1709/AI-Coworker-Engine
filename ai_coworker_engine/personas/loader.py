import yaml
from pathlib import Path

PERSONA_DIR = Path(__file__).parent

def load_persona(persona_id: str) -> dict:
    path = PERSONA_DIR / f"{persona_id}.yaml"

    if not path.exists():
        raise ValueError(f"Persona '{persona_id}' not found")

    with open(path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)    