import os
import logging
from groq import Groq
from dotenv import load_dotenv

load_dotenv()
logger = logging.getLogger(__name__)

client = Groq(api_key=os.getenv("GROQ_API_KEY"))
WHISPER_MODEL = "whisper-large-v3"

ALLOWED_AUDIO_EXTENSIONS = {".mp3", ".wav", ".m4a", ".ogg"}
MAX_AUDIO_SIZE_BYTES = 25 * 1024 * 1024  # 25 MB — Whisper API limit


class AudioTranscriptionError(Exception):
    """Raised when the Groq Whisper API fails to transcribe audio."""
    pass


def transcribe_audio(raw_bytes: bytes, filename: str) -> str:
    """
    Transcribe an audio file using Groq's Whisper API.

    Args:
        raw_bytes: The raw bytes of the audio file.
        filename: Original filename (used for extension validation and API call).

    Returns:
        The transcribed text as a string.

    Raises:
        ValueError: If the file extension is not supported or the file exceeds 25 MB.
        AudioTranscriptionError: If the Groq API call fails.
    """
    # Validate extension
    ext = ("." + filename.rsplit(".", 1)[-1].lower()) if "." in filename else ""
    if ext not in ALLOWED_AUDIO_EXTENSIONS:
        raise ValueError(
            f"Unsupported audio format '{ext}'. "
            f"Accepted formats: {', '.join(sorted(ALLOWED_AUDIO_EXTENSIONS))}"
        )

    # Validate file size
    if len(raw_bytes) > MAX_AUDIO_SIZE_BYTES:
        size_mb = len(raw_bytes) / (1024 * 1024)
        raise ValueError(
            f"Audio file is too large ({size_mb:.1f} MB). "
            f"Maximum allowed size is 25 MB."
        )

    try:
        transcription = client.audio.transcriptions.create(
            model=WHISPER_MODEL,
            file=(filename, raw_bytes),
            response_format="text",
        )
        return transcription
    except Exception as e:
        logger.error(f"Groq Whisper transcription failed: {e}")
        raise AudioTranscriptionError(
            f"Audio transcription failed: {e}"
        )
