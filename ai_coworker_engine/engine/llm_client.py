# engine/llm_client.py
import google.generativeai as genai


class GeminiLLMClient:
    """
    Thin wrapper around Google Gemini API with token limits.
    """

    def __init__(
        self,
        api_key: str,
        model: str = "gemini-2.5-flash-lite",
        max_output_tokens: int | None = None,
        max_prompt_chars: int = 6000,
        temperature: float = 0.7
    ):
        genai.configure(api_key=api_key)

        self.model_name = model
        self.model = genai.GenerativeModel(model)
        self.max_output_tokens = max_output_tokens
        self.max_prompt_chars = max_prompt_chars
        self.temperature = temperature

    def _truncate_prompt(self, prompt: str) -> str:
        if len(prompt) <= self.max_prompt_chars:
            return prompt
        # keep most recent context
        return prompt[-self.max_prompt_chars:]

    def generate(self, prompt: str) -> str:
        safe_prompt = self._truncate_prompt(prompt)

        response = self.model.generate_content(
            safe_prompt,
            generation_config={
                "max_output_tokens": self.max_output_tokens,
                "temperature": self.temperature,
            }
        )

        # Defensive handling
        text = (response.text or "").strip()

        if not text:
            return "Let’s refocus on the business scenario."

        if text[-1] not in ".!?":
            text += " …"

        return text