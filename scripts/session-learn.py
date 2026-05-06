#!/usr/bin/env python3
"""
SessionEnd hook script: extracts concepts and decisions from the most recent
Claude Code session and writes a learning note to your Obsidian vault (or any
markdown folder you configure).

This is the CAPTURE layer — it silently saves raw material after every session.
The /learn command is the ACTIVE LEARNING layer that quizzes you on it later.

Configuration:
  Set LEARN_NOTES_DIR environment variable to change where notes are written.
  Default: ~/Documents/Obsidian Vault/Learning/
"""

import json
import os
import re
import glob
from datetime import datetime
from pathlib import Path

NOTES_DIR = Path(os.environ.get(
    'LEARN_NOTES_DIR',
    os.path.expanduser('~/Documents/Obsidian Vault/Learning/')
))
CLAUDE_DIR = Path.home() / ".claude" / "projects"


def find_latest_session():
    """Find the most recently modified JSONL session file."""
    pattern = str(CLAUDE_DIR / "**" / "*.jsonl")
    files = glob.glob(pattern, recursive=True)
    if not files:
        return None
    return max(files, key=os.path.getmtime)


def extract_session_data(filepath):
    """Parse JSONL and extract user messages, assistant responses, and tool usage."""
    messages = []
    tools_used = set()
    files_touched = set()

    with open(filepath, 'r', errors='ignore') as f:
        for line in f:
            try:
                entry = json.loads(line.strip())
                msg_type = entry.get('type', '')

                if msg_type == 'user':
                    msg = entry.get('message', {})
                    if isinstance(msg, dict):
                        content = msg.get('content', '')
                        if isinstance(content, str) and len(content) > 10:
                            messages.append(('user', content[:500]))

                elif msg_type == 'assistant':
                    msg = entry.get('message', {})
                    if isinstance(msg, dict):
                        content = msg.get('content', '')
                        if isinstance(content, list):
                            for block in content:
                                if isinstance(block, dict):
                                    if block.get('type') == 'text':
                                        text = block.get('text', '')
                                        if len(text) > 20:
                                            messages.append(('assistant', text[:500]))
                                    elif block.get('type') == 'tool_use':
                                        tool = block.get('name', '')
                                        tools_used.add(tool)
                                        inp = block.get('input', {})
                                        if isinstance(inp, dict):
                                            fp = inp.get('file_path', '')
                                            if fp and isinstance(fp, str) and '/' in fp:
                                                files_touched.add(fp[:100])

            except (json.JSONDecodeError, KeyError):
                continue

    return {
        'messages': messages[-40:],
        'tools': list(tools_used),
        'files': list(files_touched)[:20],
        'total_messages': len(messages)
    }


def identify_concepts(data):
    """Simple heuristic extraction of concepts and patterns from messages."""
    concepts = set()

    tech_patterns = [
        r'\b(API|MCP|hook|skill|agent|pipeline|schema|endpoint|middleware)\b',
        r'\b(TypeScript|Python|JavaScript|CSS|HTML|SQL|JSON|YAML)\b',
        r'\b(git|commit|branch|merge|rebase|worktree)\b',
        r'\b(component|module|function|class|interface|type)\b',
        r'\b(deploy|build|test|lint|format|compile)\b',
        r'\b(database|query|migration|model|ORM)\b',
        r'\b(auth|token|session|cookie|JWT)\b',
        r'\b(webpack|vite|bun|npm|yarn)\b',
    ]

    for role, text in data['messages']:
        for pattern in tech_patterns:
            matches = re.findall(pattern, text, re.IGNORECASE)
            concepts.update(m.lower() for m in matches)

    return list(concepts)[:15]


def write_learning_note(data, concepts):
    """Write a learning note to the configured directory."""
    NOTES_DIR.mkdir(parents=True, exist_ok=True)

    now = datetime.now()
    date_str = now.strftime('%Y-%m-%d')
    time_str = now.strftime('%H:%M')

    existing = list(NOTES_DIR.glob(f'{date_str}*.md'))
    suffix = f'-{len(existing) + 1}' if existing else ''
    filename = f'{date_str}{suffix}.md'
    filepath = NOTES_DIR / filename

    tools_str = ', '.join(data['tools'][:10]) if data['tools'] else 'none captured'
    files_str = '\n'.join(f'- `{f}`' for f in data['files'][:10]) if data['files'] else '- none captured'
    concepts_str = ', '.join(concepts) if concepts else 'none identified'

    summary_parts = []
    for role, text in data['messages'][-6:]:
        if role == 'assistant' and len(text) > 50:
            summary_parts.append(text[:200])
    summary = ' ... '.join(summary_parts[-2:]) if summary_parts else 'No summary available'

    note = f"""# Session Learning — {date_str} {time_str}

**Messages exchanged:** {data['total_messages']}
**Tools used:** {tools_str}
**Concepts touched:** {concepts_str}

## Files touched
{files_str}

## Session context
{summary[:500]}

## Review prompts
- What patterns or concepts from this session would I struggle to explain to someone else?
- Did I encounter any errors? Do I understand WHY they happened, not just how they were fixed?
- What decisions were made? Could I defend them?

---
*Auto-generated by SessionEnd hook. Run `/learn` for active quiz on these concepts.*
"""

    filepath.write_text(note)
    return str(filepath)


def main():
    session_file = find_latest_session()
    if not session_file:
        return

    data = extract_session_data(session_file)
    if data['total_messages'] < 5:
        return

    concepts = identify_concepts(data)
    note_path = write_learning_note(data, concepts)
    print(f"Learning note written: {note_path}")


if __name__ == '__main__':
    main()
