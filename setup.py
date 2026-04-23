#!/usr/bin/env python3
"""Run this once to create your .env file."""
import os

env_path = os.path.join(os.path.dirname(__file__), ".env")

print("Darkroom Master Pro — Setup")
print("=" * 40)
anthropic_key = input("Paste your ANTHROPIC_API_KEY: ").strip()
openai_key = input("Paste your OPENAI_API_KEY: ").strip()

lines = [f"ANTHROPIC_API_KEY={anthropic_key}", f"OPENAI_API_KEY={openai_key}", ""]
with open(env_path, "w") as f:
    f.write("\n".join(lines))

print(f"\n.env created at {env_path}")
print("Run:  python workflow.py")
