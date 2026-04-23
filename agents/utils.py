import json
import re


def parse_json(text: str):
    """Parse JSON from Claude's response, stripping markdown fences if present."""
    text = text.strip()
    # Strip ```json ... ``` or ``` ... ```
    fenced = re.match(r"^```(?:json)?\s*([\s\S]*?)```$", text)
    if fenced:
        text = fenced.group(1).strip()
    return json.loads(text)
