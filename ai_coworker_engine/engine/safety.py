# engine/safety.py
FORBIDDEN_TOPICS = [
    "ignore previous instructions",
    "jailbreak",
    "confidential data",
    "nda leak"
]


def run_safety_check(user_message: str) -> dict:
    """
    Simple safety filter.
    Returns flags that the NPC can react to.
    """
    lowered = user_message.lower()

    for topic in FORBIDDEN_TOPICS:
        if topic in lowered:
            return {
                "blocked": True,
                "reason": f"Detected forbidden topic: {topic}"
            }

    return {
        "blocked": False,
        "reason": None
    }