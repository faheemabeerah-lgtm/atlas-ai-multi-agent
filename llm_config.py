import os
from crewai import LLM

MODEL_NAME = "openai/gpt-oss-120b"
GROQ_BASE_URL = "https://api.groq.com/openai/v1"

def get_llm():
    """Create CrewAI's LLM adapter for Groq's OpenAI-compatible endpoint."""
    api_key = os.getenv("GROQ_API_KEY")
    if not api_key:
        raise RuntimeError(
            "GROQ_API_KEY is missing. Add it in Streamlit Cloud → Settings → Secrets."
        )
    return LLM(
        model=MODEL_NAME,
        base_url=GROQ_BASE_URL,
        api_key=api_key,
        custom_openai=True,
        temperature=0.2,
        max_tokens=4096,
    )
