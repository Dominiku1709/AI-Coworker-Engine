# engine/director.py

from engine.state import NPCState


class Director:
    """
    Invisible supervisor that ensures the simulation stays on track.
    """

    def __init__(self):
        self.loop_threshold = 3
        self.frustration_threshold = 0.6

        self.simulation_keywords = {
            "talent", "leadership", "brand", "kpi",
            "mobility", "competency", "development", "hr"
        }

        self.progress_verbs = {
            "propose", "decide", "prioritize",
            "align", "recommend", "define"
        }

    def evaluate(self, state: NPCState) -> dict:
        # Frustration
        if state.frustration_level >= self.frustration_threshold:
            return self._intervene(
                "high_frustration",
                "Let’s reset. What outcome matters most at group level?"
            )

        # Looping
        if self._is_looping(state):
            return self._intervene(
                "looping",
                "We’re circling. Please propose one concrete option and its trade-offs."
            )

        # Off-topic
        if self._is_off_topic(state):
            return self._intervene(
                "off_topic",
                "Let’s bring this back to the leadership and talent scenario."
            )

        # No progress
        if self._no_progress(state):
            return self._intervene(
                "no_progress",
                "What decision or recommendation would you like to land?"
            )

        return {"intervene": False, "reason": None, "hint": None}

    def _intervene(self, reason: str, hint: str) -> dict:
        return {"intervene": True, "reason": reason, "hint": hint}

    def _is_looping(self, state: NPCState) -> bool:
        user_turns = [t["content"] for t in state.conversation_history if t["role"] == "user"]
        if len(user_turns) < self.loop_threshold:
            return False
        recent = user_turns[-self.loop_threshold:]
        return len(set(recent)) == 1

    def _is_off_topic(self, state: NPCState) -> bool:
        last_user = next(
            (t["content"].lower() for t in reversed(state.conversation_history) if t["role"] == "user"),
            ""
        )
        if not last_user:
            return False

        keyword_overlap = any(k in last_user for k in self.simulation_keywords)
        return not keyword_overlap

    def _no_progress(self, state: NPCState) -> bool:
        if len(state.conversation_history) < 6:
            return False

        last_user = next(
            (t["content"].lower() for t in reversed(state.conversation_history) if t["role"] == "user"),
            ""
        )

        return not any(v in last_user for v in self.progress_verbs)