import json
from app.llm_service import generate_meeting_minutes

with open("samples/transcript_short.txt") as f:
    transcript = f.read()

result = generate_meeting_minutes(transcript)
print(json.dumps(result, indent=2))