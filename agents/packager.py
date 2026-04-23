import json
from datetime import datetime
from pathlib import Path


def package_content(run_id: str, strategy: dict, image_path: str, captions: dict) -> str:
    output_dir = Path("output") / run_id
    output_dir.mkdir(parents=True, exist_ok=True)

    (output_dir / "captions.json").write_text(json.dumps(captions, indent=2))

    metadata = {
        "run_id": run_id,
        "generated_at": datetime.now().isoformat(),
        "strategy": strategy,
        "files": {
            "image": "post_image.png",
            "captions": "captions.json",
            "metadata": "metadata.json",
            "summary": "content_summary.txt",
        },
    }
    (output_dir / "metadata.json").write_text(json.dumps(metadata, indent=2))

    all_hashtags = (
        strategy.get("hashtags", {}).get("primary", [])
        + strategy.get("hashtags", {}).get("secondary", [])
        + strategy.get("hashtags", {}).get("niche", [])
    )

    summary_lines = [
        "DARKROOM MASTER PRO — Content Package",
        f"Run ID  : {run_id}",
        f"Created : {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
        "",
        f"TOPIC       : {strategy.get('topic', '')}",
        f"ANGLE       : {strategy.get('angle', '')}",
        f"AUDIENCE    : {strategy.get('target_audience', '')}",
        f"KEY MESSAGE : {strategy.get('key_message', '')}",
        f"HASHTAGS    : {' '.join(all_hashtags)}",
        "",
        "─" * 60,
        "INSTAGRAM",
        "─" * 60,
        captions.get("instagram", ""),
        "",
        "─" * 60,
        "FACEBOOK",
        "─" * 60,
        captions.get("facebook", ""),
        "",
        "─" * 60,
        "TWITTER / X",
        "─" * 60,
        captions.get("twitter", ""),
        "",
        "─" * 60,
        "LINKEDIN",
        "─" * 60,
        captions.get("linkedin", ""),
    ]
    (output_dir / "content_summary.txt").write_text("\n".join(summary_lines))

    return str(output_dir)
