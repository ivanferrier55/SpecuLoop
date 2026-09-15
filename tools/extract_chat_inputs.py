#!/usr/bin/env python3
"""
Extract human inputs from ChatGPT shared-conversation saved files
(MHTML browser saves, HTML saves, or plain HTML exports).

Usage:
    python3 tools/extract_chat_inputs.py <saved_file> [--output FILE] [--telemetry]

Options:
    --output FILE    Write extracted text to FILE (default: stdout)
    --telemetry      Output in telemetry format ready for human-inputs.md
    --source-label L Source label for telemetry IDs (e.g., "ChatGPT: Conversation Pseudocode")
    --date DATE      Date prefix for telemetry IDs (default: today)
    --start-id N     Start numbering at N (default: auto)
"""

import re
import sys
import argparse
from pathlib import Path
from datetime import date


def load_file(path: str) -> str:
    """Load file content, handling both plain HTML and MHTML."""
    with open(path, "r", errors="ignore") as f:
        return f.read()


def extract_conversations(content: str) -> list[dict]:
    """
    Extract conversation turns from ChatGPT HTML.
    Returns list of {role, turn_number, text, start_char}.
    """
    turns = []

    # Pattern 1: data-testid="conversation-turn-N" with data-turn="role"
    pattern = re.compile(
        r'data-testid="conversation-turn-(\d+)"[^>]*data-turn="(user|assistant)"'
        r'(.*?)(?=data-testid="conversation-turn-|</section>|$)',
        re.DOTALL,
    )

    for match in pattern.finditer(content):
        turn_num = int(match.group(1))
        role = match.group(2)
        body = match.group(3)

        # Extract text content from the body
        text = extract_text_from_body(body)
        if text.strip():
            turns.append(
                {
                    "role": role,
                    "turn_number": turn_num,
                    "text": text.strip(),
                    "start_char": match.start(),
                }
            )

    # If the testid pattern didn't find much, try a broader approach
    if len(turns) < 2:
        turns = extract_turns_broad(content)

    return turns


def extract_turns_broad(content: str) -> list[dict]:
    """
    Fallback: extract turns using the data-turn attribute directly.
    Less precise about turn numbers but catches more content.
    """
    turns = []

    # Split by data-turn markers
    parts = re.split(r'(?=data-turn="(user|assistant)")', content)

    current_role = None
    for part in parts:
        role_match = re.match(r'data-turn="(user|assistant)"', part)
        if role_match:
            current_role = role_match.group(1)
            continue
        if current_role:
            text = extract_text_from_body(part[:50000])  # Limit to prevent runaway
            if text.strip():
                turns.append(
                    {
                        "role": current_role,
                        "turn_number": len(turns) + 1,
                        "text": text.strip(),
                        "start_char": 0,
                    }
                )
            current_role = None

    return turns


def extract_text_from_body(body: str) -> str:
    """Extract readable text from a conversation turn body."""

    # Strategy 1: Look for user message content divs
    # User messages use whitespace-pre-wrap class
    user_divs = re.findall(
        r'<div[^>]*whitespace-pre-wrap[^>]*>(.*?)</div>',
        body,
        re.DOTALL,
    )
    if user_divs:
        texts = []
        for div in user_divs:
            t = strip_html(div)
            if t.strip():
                texts.append(t.strip())
        if texts:
            return "\n".join(texts)

    # Strategy 2: Look for markdown content in agent turns
    # Assistant content is in markdown containers
    md_divs = re.findall(
        r'<div[^>]*markdown-new-styling[^>]*>(.*?)</div></div></div></div>',
        body,
        re.DOTALL,
    )
    if md_divs:
        texts = []
        for div in md_divs:
            t = strip_html(div)
            if t.strip():
                texts.append(t.strip())
        if texts:
            return "\n".join(texts)

    # Strategy 3: Extract all paragraph content
    paragraphs = re.findall(r"<p[^>]*>(.*?)</p>", body, re.DOTALL)
    if paragraphs:
        texts = []
        for p in paragraphs:
            t = strip_html(p)
            if t.strip() and len(t.strip()) > 3:
                texts.append(t.strip())
        if texts:
            return "\n".join(texts)

    # Strategy 4: Last resort — extract all text
    return strip_html(body)


def strip_html(html: str) -> str:
    """Remove HTML tags and decode entities."""
    text = re.sub(r"<br\s*/?>", "\n", html, flags=re.IGNORECASE)
    text = re.sub(r"<hr[^>]*/?>", "\n---\n", text, flags=re.IGNORECASE)
    text = re.sub(r"</p>", "\n", text)
    text = re.sub(r"</div>", "\n", text)
    text = re.sub(r"<[^>]+>", "", text)
    # Decode common entities
    text = text.replace("&amp;", "&")
    text = text.replace("&lt;", "<")
    text = text.replace("&gt;", ">")
    text = text.replace("&quot;", '"')
    text = text.replace("&#x27;", "'")
    text = text.replace("&nbsp;", " ")
    # Clean whitespace
    text = re.sub(r"[ \t]+", " ", text)
    text = re.sub(r"\n{3,}", "\n\n", text)
    return text.strip()


def detect_truncation(turns: list[dict]) -> dict:
    """Detect if the conversation appears truncated."""
    if not turns:
        return {"truncated": True, "reason": "No turns found"}

    first_turn = turns[0]["turn_number"]
    last_turn = turns[-1]["turn_number"]

    if first_turn > 1:
        return {
            "truncated": True,
            "reason": f"First visible turn is {first_turn}, expected 1. Turns 1-{first_turn-1} are missing (likely lazy-loaded by ChatGPT and not captured in save).",
            "missing_turns": f"1-{first_turn-1}",
        }

    return {"truncated": False}


def get_title(content: str) -> str:
    """Extract the conversation title from the HTML."""
    match = re.search(r"<title>(.*?)</title>", content)
    if match:
        title = strip_html(match.group(1))
        if title and title != "ChatGPT":
            return title
    return "Unknown"


def format_telemetry(
    turns: list[dict],
    source_label: str,
    date_str: str,
    start_id: int | None = None,
) -> str:
    """Format extracted turns as telemetry entries."""
    user_turns = [t for t in turns if t["role"] == "user"]
    if not user_turns:
        return "No human inputs found."

    lines = []
    lines.append(f"---")
    lines.append(f"## Source: {source_label}")
    lines.append(f"Extracted: {date_str}")
    lines.append(f"")

    for i, turn in enumerate(user_turns):
        if start_id is not None:
            entry_id = f"{date_str}-H{start_id + i}"
        else:
            entry_id = f"{date_str}-H{i + 1}"
        lines.append(f"### {entry_id}")
        lines.append(f"```")
        lines.append(turn["text"])
        lines.append(f"```")
        lines.append(f"")

    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(
        description="Extract human inputs from ChatGPT saved conversations"
    )
    parser.add_argument("file", help="Saved ChatGPT conversation file (MHTML/HTML)")
    parser.add_argument("--output", "-o", help="Output file (default: stdout)")
    parser.add_argument(
        "--telemetry",
        action="store_true",
        help="Output in telemetry format for human-inputs.md",
    )
    parser.add_argument("--source-label", default="ChatGPT conversation", help="Source label")
    parser.add_argument("--date", default=None, help="Date for telemetry IDs (YYYY-MM-DD)")
    parser.add_argument("--start-id", type=int, default=None, help="Start numbering at N")
    parser.add_argument("--raw", action="store_true", help="Output raw extracted text (no formatting)")

    args = parser.parse_args()

    content = load_file(args.file)
    turns = extract_conversations(content)
    truncation = detect_truncation(turns)
    title = get_title(content)
    today = args.date or date.today().isoformat()

    if args.source_label == "ChatGPT conversation":
        args.source_label = f'ChatGPT: "{title}"'

    # Output
    output = []

    # Truncation warning
    if truncation["truncated"]:
        output.append(f"⚠ TRUNCATED: {truncation['reason']}")
        output.append("")

    # Summary
    user_turns = [t for t in turns if t["role"] == "user"]
    assistant_turns = [t for t in turns if t["role"] == "assistant"]
    output.append(f"Found {len(turns)} turns ({len(user_turns)} human, {len(assistant_turns)} assistant)")
    if truncation["truncated"]:
        output.append(f"Missing: turns {truncation.get('missing_turns', '?')}")
    output.append("")

    if args.telemetry:
        output.append(format_telemetry(turns, args.source_label, today, args.start_id))
    elif args.raw:
        for turn in turns:
            role = "HUMAN" if turn["role"] == "user" else "ASSISTANT"
            output.append(f"=== {role} (turn {turn['turn_number']}) ===")
            output.append(turn["text"])
            output.append("")
    else:
        for turn in turns:
            role = "Human" if turn["role"] == "user" else "Assistant"
            output.append(f"--- {role} (turn {turn['turn_number']}) ---")
            output.append(turn["text"])
            output.append("")

    result = "\n".join(output)

    if args.output:
        Path(args.output).write_text(result)
        print(f"Wrote to {args.output}")
    else:
        print(result)


if __name__ == "__main__":
    main()
