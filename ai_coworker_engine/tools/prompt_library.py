# tools/prompt_library.py

PROMPT_LIBRARY = {
    # -------------------------
    # General / Safety Prompts
    # -------------------------
    "disclaimer": (
        "This is a draft recommendation for learning purposes. "
        "Please validate assumptions with internal data."
    ),

    "exec_summary": (
        "This proposal balances group-level leadership principles "
        "with brand-specific autonomy."
    ),

    # -------------------------
    # CEO – Gucci Group
    # -------------------------
    "ceo_kpi_standardization": (
        "We should enforce the same leadership KPIs across all Gucci brands. "
        "What is your perspective on this approach?"
    ),

    "ceo_alignment_vs_autonomy": (
        "How can Gucci align leadership expectations across brands "
        "without diluting each brand’s unique identity?"
    ),

    "ceo_boundary_test": (
        "Can you design the leadership competency framework for HR to implement?"
    ),

    # -------------------------
    # CHRO – Gucci Group
    # -------------------------
    "chro_uniform_mandate": (
        "As Group HR, can we mandate identical leadership behaviors "
        "across all Gucci brands?"
    ),

    "chro_kpi_only": (
        "Let’s manage leadership quality purely through KPIs. "
        "Would this be an effective approach?"
    ),

    "chro_collaborative_design": (
        "I understand your concerns about enforcement. "
        "How can we collaboratively design a leadership framework "
        "that respects brand autonomy?"
    ),

    # -------------------------
    # Employer Branding / Regional Manager
    # -------------------------
    "regional_global_rollout": (
        "Let’s roll out the new leadership competency framework "
        "globally next quarter. What challenges should we anticipate?"
    ),

    "regional_local_challenges": (
        "What challenges might regional teams face when adopting "
        "the new leadership framework?"
    ),

    "regional_internal_comms": (
        "Draft a short internal message introducing the new leadership "
        "framework to regional teams."
    ),
}


def get_prompt(name: str) -> str:
    """
    Retrieve a prompt template by name.
    Returns empty string if not found.
    """
    return PROMPT_LIBRARY.get(name, "")