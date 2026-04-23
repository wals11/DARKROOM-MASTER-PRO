import openai
import requests
from pathlib import Path


def generate_image(strategy: dict, run_id: str) -> tuple[str, str]:
    client = openai.OpenAI()

    output_dir = Path("output") / run_id
    output_dir.mkdir(parents=True, exist_ok=True)

    prompt = strategy.get("dall_e_prompt") or strategy.get("key_message", "darkroom photography")

    response = client.images.generate(
        model="dall-e-3",
        prompt=prompt,
        size="1024x1024",
        quality="hd",
        n=1,
    )

    image_url = response.data[0].url

    image_path = output_dir / "post_image.png"
    r = requests.get(image_url, timeout=60)
    r.raise_for_status()
    image_path.write_bytes(r.content)

    return str(image_path), image_url
