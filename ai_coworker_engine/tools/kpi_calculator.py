# tools/kpi_calculator.py

def evaluate_kpi(kpi_name: str, scope: str) -> dict:
    """
    Fake but deterministic KPI evaluator.
    """
    risk_map = {
        "group": "High risk of brand misalignment",
        "brand": "Medium risk, manageable with autonomy",
        "local": "Low risk, context-aware"
    }

    return {
        "kpi": kpi_name,
        "scope": scope,
        "risk": risk_map.get(scope, "Unknown"),
        "recommendation": (
            "Avoid uniform enforcement"
            if scope == "group"
            else "Proceed with contextual adaptation"
        )
    }