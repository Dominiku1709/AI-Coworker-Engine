# engine/state.py
from dataclasses import dataclass, field
from typing import List, Dict


@dataclass
class NPCState:
    """
    Short-term conversational state for an NPC.
    Lives per user-session.
    """
    conversation_history: List[Dict[str, str]] = field(default_factory=list)

    relationship_score: float = 0.5  # 0 = hostile, 1 = trusted
    frustration_level: float = 0.0   # increases if user is annoying
    is_blocked: bool = False

    def update_relationship(self, delta: float):
        self.relationship_score = min(max(self.relationship_score + delta, 0.0), 1.0)

    def update_frustration(self, delta: float):
        self.frustration_level = min(max(self.frustration_level + delta, 0.0), 1.0)