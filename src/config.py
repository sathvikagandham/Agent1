"""Configuration and constants for the self-healing code agent."""

from dotenv import load_dotenv
load_dotenv()  # Must run before anything reads GROQ_API_KEY

MODEL = "llama-3.3-70b-versatile"
MAX_REQUESTS = 8      # Max LLM calls per task
EXEC_TIMEOUT = 10     # Seconds before killing runaway subprocess