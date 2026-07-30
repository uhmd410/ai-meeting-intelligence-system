import os
import json
import time
import logging
from groq import Groq
from dotenv import load_dotenv
from pydantic import ValidationError

from app.prompts.meeting_minutes_prompt import SYSTEM_PROMPT, build_user_prompt
from app.schemas.llm_output import LLMMeetingMinutes

load_dotenv()
logger = logging.getLogger(__name__)

client = Groq(api_key=os.getenv("GROQ_API_KEY"))
MODEL_NAME = "llama-3.3-70b-versatile"


class LLMGenerationError(Exception):
    """Raised when the LLM fails to produce valid structured output after retries."""
    pass


def _call_groq(messages: list) -> str:
    response = client.chat.completions.create(
        model=MODEL_NAME,
        messages=messages,
        temperature=0.2,  # low temperature for consistent structure
    )
    return response.choices[0].message.content


def _strip_code_fences(text: str) -> str:
    """Defensive cleanup in case the model wraps output in ```json ... ``` anyway."""
    text = text.strip()
    if text.startswith("```"):
        text = text.split("```")[1]
        text = text.replace("json", "", 1).strip() if text.lower().startswith("json") else text.strip()
    return text.strip()


def generate_meeting_minutes(transcript: str) -> dict:
    """
    Sends a transcript to the Groq LLM and returns validated, structured meeting minutes.
    Retries once with a corrective message if the first response isn't valid JSON.
    """
    messages = [
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": build_user_prompt(transcript)},
    ]

    start = time.time()
    raw_output = _call_groq(messages)
    elapsed = time.time() - start
    logger.info(f"Groq call completed in {elapsed:.2f}s")

    cleaned = _strip_code_fences(raw_output)

    try:
        parsed = json.loads(cleaned)
        validated = LLMMeetingMinutes(**parsed)
        return validated.model_dump()
    except (json.JSONDecodeError, ValidationError) as e:
        logger.warning(f"First attempt failed validation: {e}. Retrying with correction.")

        correction_messages = messages + [
            {"role": "assistant", "content": raw_output},
            {"role": "user", "content": (
                "Your previous response was not valid JSON matching the required structure. "
                "Return ONLY the corrected valid JSON object, with no extra text or markdown."
            )},
        ]
        retry_output = _call_groq(correction_messages)
        retry_cleaned = _strip_code_fences(retry_output)

        try:
            parsed_retry = json.loads(retry_cleaned)
            validated_retry = LLMMeetingMinutes(**parsed_retry)
            return validated_retry.model_dump()
        except (json.JSONDecodeError, ValidationError) as e2:
            logger.error(f"Retry also failed: {e2}")
            raise LLMGenerationError(
                f"Failed to generate valid meeting minutes after retry: {e2}"
            )