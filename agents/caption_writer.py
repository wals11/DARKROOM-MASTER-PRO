import json
import anthropic
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
    client = anthropic.Anthropic()

    response = client.messages.create(
        model="claude-haiku-4-5-20251001",
        max_tokens=3000,
        system=[{"type": "text", "text": _SYSTEM, "cache_control": {"type": "ephemeral"}}],
        messages=[{
            "role": "user",
            "content": (
                f"Write platform-specific captions for this content strategy:\n\n"
                f"{json.dumps(strategy, indent=2)}\n\n"
                "Return a JSON object only — no prose, no markdown fences:\n"
                "{\n"
                "  \"instagram\": \"...\",\n"
                "  \"facebook\": \"...\",\n"
                "  \"twitter\": \"...\",\n"
                "  \"linkedin\": \"...\"\n"
                "}"
            )
        }]
    )

    return parse_json(response.content[0].text)
