import json
from agents.utils import gemini, parse_json

_SYSTEM = """\
You are the content strategist for Darkroom Master Pro — a brand dedicated to darkroom photography \
education and inspiration. You select the single best topic from a research list and build a complete \
content strategy: angle, tone, key message, DALL-E image prompt, and hashtag sets. \
Your content is technically accurate, visually compelling, and authentic to the analog community."""


def strategize_content(topics: list[dict]) -> dict:
    prompt = (
        f"Here are today's researched topics:\n\n{json.dumps(topics, indent=2)}\n\n"
        "Select the BEST topic for a social media post and return a complete strategy.\n\n"
        "Return a JSON object only — no prose, no markdown fences:\n"
        "{\n"
        "  \"topic\": \"selected topic name\",\n"
        "  \"angle\": \"specific content hook\",\n"
        "  \"target_audience\": \"who this is for\",\n"
        "  \"tone\": \"e.g. educational, inspirational, technical\",\n"
        "  \"key_message\": \"the single main takeaway\",\n"
        "  \"dall_e_prompt\": \"optimized DALL-E 3 prompt — photorealistic, dramatic, darkroom-themed\",\n"
        "  \"hashtags\": {\n"
        "    \"primary\": [\"#tag\"],\n"
        "    \"secondary\": [\"#tag\"],\n"
        "    \"niche\": [\"#tag\"]\n"
        "  },\n"
        "  \"selection_reason\": \"why this topic was chosen\"\n"
        "}"
    )
    return parse_json(gemini(prompt, _SYSTEM))
