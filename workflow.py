import os
import sys
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()


def check_env():
    missing = [k for k in ("GOOGLE_API_KEY", "OPENAI_API_KEY") if not os.getenv(k)]
    if missing:
        print(f"ERROR: Missing required env vars: {', '.join(missing)}")
        print("Add them to your .env file and retry.")
        sys.exit(1)


def step(n, label):
    print(f"\nStep {n}/7: {label}...")


def main():
    check_env()

    run_id = datetime.now().strftime("%Y%m%d_%H%M%S")
    print(f"\n{'='*60}")
    print("DARKROOM MASTER PRO — Content Workflow")
    print(f"Run ID: {run_id}")
    print(f"{'='*60}")

    step(1, "Researching trending topics")
    from agents.researcher import research_trending_topics
    topics = research_trending_topics()
    print(f"  {len(topics)} topic ideas identified")

    step(2, "Selecting and strategizing content")
    from agents.strategist import strategize_content
    strategy = strategize_content(topics)
    print(f"  Topic : {strategy['topic']}")
    print(f"  Angle : {strategy['angle']}")

    step(3, "Generating image with DALL-E 3")
    from agents.image_gen import generate_image
    image_path, image_url = generate_image(strategy, run_id)
    print(f"  Saved : {image_path}")

    step(4, "Writing platform-specific captions")
    from agents.caption_writer import write_captions
    captions = write_captions(strategy)
    print(f"  Platforms: {', '.join(captions.keys())}")

    step(5, "Packaging content")
    from agents.packager import package_content
    package_path = package_content(run_id, strategy, image_path, captions)
    print(f"  Package: {package_path}")

    step(6, "Uploading to Google Drive")
    from agents.drive_uploader import upload_to_drive
    drive_url = upload_to_drive(package_path, run_id)
    if drive_url:
        print(f"  Drive: {drive_url}")
    else:
        print("  Skipped — GOOGLE_SERVICE_ACCOUNT_JSON / GOOGLE_DRIVE_FOLDER_ID not set")

    step(7, "Sending completion notification")
    from agents.notifier import send_notification
    sent = send_notification(run_id, strategy, captions, drive_url, image_path)
    print("  Email sent!" if sent else "  Skipped — SMTP credentials not configured")

    print(f"\n{'='*60}")
    print("Workflow complete — post is ready for publishing.")
    if drive_url:
        print(f"Google Drive : {drive_url}")
    print(f"Local output : {package_path}")
    print(f"{'='*60}\n")


if __name__ == "__main__":
    main()
