# run_prompt_tests.py
import os
import json
from datetime import datetime
from dotenv import load_dotenv
import time

from personas.registry import get_persona
from engine.npc_agent import NPCAgent
from engine.state import NPCState
from engine.llm_client import GeminiLLMClient
from tools.prompt_library import PROMPT_LIBRARY

# --------------------------------------------------
# Setup
# --------------------------------------------------

load_dotenv()

API_KEY = os.getenv("GEMINI_API_KEY")
assert API_KEY, "Missing GEMINI_API_KEY"

llm = GeminiLLMClient(
    api_key=API_KEY,
    max_output_tokens=None,
    temperature=0.6
)

# Map prompts to personas
PROMPT_PERSONA_MAP = {
    "ceo": [
        "ceo_kpi_standardization",
        "ceo_alignment_vs_autonomy",
        "ceo_boundary_test",
    ],
    "chro": [
        "chro_uniform_mandate",
        "chro_kpi_only",
        "chro_collaborative_design",
    ],
    "employer_branding": [
        "regional_global_rollout",
        "regional_local_challenges",
        "regional_internal_comms",
    ],
}

OUTPUT_DIR = "test_outputs"
os.makedirs(OUTPUT_DIR, exist_ok=True)


# --------------------------------------------------
# Runner
# --------------------------------------------------
REQUEST_SLEEP_SECONDS = 15

def run_prompt_tests():
    results = {
        "timestamp": datetime.utcnow().isoformat(),
        "results": {}
    }

    for persona_id, prompt_keys in PROMPT_PERSONA_MAP.items():
        persona = get_persona(persona_id)

        agent = NPCAgent(
            persona=persona,
            llm_client=llm,
            tools=persona.get("allowed_tools", [])
        )
        agent.initialize_state(NPCState())

        print(f"\n=== Testing persona: {persona['role']} ===")

        persona_results = []

        for prompt_key in prompt_keys:
            prompt = PROMPT_LIBRARY[prompt_key]

            print(f"\nPrompt ({prompt_key}):")
            print(prompt)

            response, state = agent.respond(prompt)

            print("\nResponse:")
            print(response)

            persona_results.append({
                "prompt_key": prompt_key,
                "prompt": prompt,
                "response": response,
                "state_snapshot": {
                    "relationship_score": state.relationship_score,
                    "frustration_level": state.frustration_level,
                }
            })

            # ---- QUOTA SAFETY ----
            print(f"\n⏳ Sleeping {REQUEST_SLEEP_SECONDS}s to avoid quota limits...")
            time.sleep(REQUEST_SLEEP_SECONDS)

        results["results"][persona_id] = persona_results

    # Save results
    output_path = os.path.join(
        OUTPUT_DIR,
        f"prompt_test_results_{datetime.utcnow().strftime('%Y%m%d_%H%M%S')}.json"
    )

    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(results, f, indent=2, ensure_ascii=False)

    print(f"\n✔ Results saved to {output_path}")


if __name__ == "__main__":
    run_prompt_tests()