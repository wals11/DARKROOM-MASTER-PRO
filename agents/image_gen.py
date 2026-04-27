import struct
import zlib
import openai
import requests
from pathlib import Path


def generate_image(strategy: dict, run_id: str) -> tuple[str, str]:
    output_dir = Path("output") / run_id
    output_dir.mkdir(parents=True, exist_ok=True)
    image_path = output_dir / "post_image.png"

    prompt = strategy.get("dall_e_prompt") or strategy.get("key_message", "darkroom photography")

    try:
        client = openai.OpenAI()
        response = client.images.generate(
            model="dall-e-3",
            prompt=prompt,
            size="1024x1024",
            quality="hd",
            n=1,
        )
        image_url = response.data[0].url
        r = requests.get(image_url, timeout=60)
        r.raise_for_status()
        image_path.write_bytes(r.content)
        return str(image_path), image_url

    except Exception as exc:
        print(f"  DALL-E unavailable ({exc.__class__.__name__}): generating placeholder")
        image_path.write_bytes(_placeholder_png())
        return str(image_path), ""


def _placeholder_png() -> bytes:
    """Generate a minimal 1x1 black PNG without external dependencies."""
    def chunk(name: bytes, data: bytes) -> bytes:
        c = name + data
        return struct.pack(">I", len(data)) + c + struct.pack(">I", zlib.crc32(c) & 0xFFFFFFFF)

    signature = b"\x89PNG\r\n\x1a\n"
    ihdr = chunk(b"IHDR", struct.pack(">IIBBBBB", 1, 1, 8, 2, 0, 0, 0))
    raw = b"\x00\x00\x00\x00"  # filter byte + 1 black RGB pixel
    idat = chunk(b"IDAT", zlib.compress(raw))
    iend = chunk(b"IEND", b"")
    return signature + ihdr + idat + iend
