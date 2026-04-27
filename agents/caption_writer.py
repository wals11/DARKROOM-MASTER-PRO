import os
import json
from google import genai
from google.genai import types
from agents.utils import parse_json

_SYSTEM = """\
You are the social media copywriter for Darkroom Master Pro. You write platform-optimized captions \
that drive engagement and reflect genuine expertise in darkroom and analog photography.

Platform conventions:
- Instagram: visual/emotional, emojis, line breaks for readability, full hashtag block at end, max 2200 chars
- Facebook: community-focused storytelling, ends with an engagement question, 3-5 hashtags, max 400 words
- Twitter/X: punchy and conversational, under 280 characters total, 2-3 inline hashtags
- LinkedIn: professional and educational, insight-driven, minimal hashtags, max 1500 chars"""


def write_captions(strategy: dict) -> dict[str, str]:
    client = genai.Client(api_key=os.getenv("GOOGLE_API_KEY"))

    response = client.models.generate_content(
        model="gemini-2.0-flash",
        contents=(
            f"Write platform-specific captions for this content strategy:\n\n"
            f"{json.dumps(strategy, indent=2)}\n\n"
            "Return a JSON object only — no prose, no markdown fences:\n"
            "{\n"
            "  \"instagram\": \"...\",\n"
            "  \"facebook\": \"...\",\n"
            "  \"twitter\": \"...\",\n"
            "  \"linkedin\": \"...\"\n"
            "}"
        ),
        config=types.GenerateContentConfig(
            system_instruction=_SYSTEM,
            max_output_tokens=3000,
        ),
    )

    return parse_json(response.text)
