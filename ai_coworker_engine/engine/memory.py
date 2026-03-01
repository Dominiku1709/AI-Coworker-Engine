# engine/memory.py
class NPCMemory:
    """
    Long-term memory.
    In a real system, this would connect to a vector DB (FAISS, Pinecone, etc.)
    """

    def __init__(self):
        self.events = []

    def store_event(self, text: str):
        self.events.append(text)

    def summarize(self) -> str:
        if not self.events:
            return "No significant past interactions."
        return " | ".join(self.events[-5:])