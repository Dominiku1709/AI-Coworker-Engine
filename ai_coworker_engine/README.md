## Design Highlights

### AI Engineering
- Persona-driven agent instantiation
- Stateless API with session-scoped NPC state
- Tool-aware NPC responses

### AI Ops & Scalability
- FastAPI service boundary
- Pluggable LLM providers
- Vector memory abstraction (FAISS)

### System Design
- Director (Supervisor) agent controls pacing
- Clear separation between persona, state, and orchestration
- One engine supports multiple NPC roles