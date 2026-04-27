from agents.utils import gemini, parse_json

_SYSTEM = """\
You are a social media content researcher specializing in darkroom photography, analog film, \
and traditional photographic processes. You identify trending topics, techniques, and conversations \
in the global analog photography community based on your knowledge of the space."""

_PROMPT = (
    "Identify 8 trending and high-potential topics in darkroom and analog photography "
    "for social media content today. Consider: darkroom techniques, film stocks, "
    "chemistry, printing methods, equipment, artistic movements, community discussions, "
    "and beginner education.\n\n"
    "Return a JSON array only — no prose, no markdown fences:\n"
    "[\n"
    "  {\n"
    "    \"topic\": \"topic name\",\n"
    "    \"description\": \"one sentence description\",\n"
    "    \"trend_reason\": \"why this resonates right now\",\n"
    "    \"content_potential\": \"high|medium|low\",\n"
    "    \"visual_potential\": \"brief image concept\"\n"
    "  }\n"
    "]"
)


def research_trending_topics() -> list[dict]:
    return parse_json(gemini(_PROMPT, _SYSTEM))
