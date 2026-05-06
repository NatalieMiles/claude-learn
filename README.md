# claude-learn

An active learning system for Claude Code that turns coding sessions into durable knowledge — not just familiarity.

## The problem

Claude Code makes you productive fast. You build things, ship features, fix bugs. But there's a gap between *doing* and *understanding*. You can use a git worktree without knowing why it helps. You can accept a hook configuration without understanding when a skill would be better. You can fix an error without learning what caused it.

Anthropic's own research ([AI Fluency Index](https://www.anthropic.com/research/ai-fluency)) found the same pattern at scale: **Description** skills (telling AI what you want) grow naturally with practice, but **Discernment** skills (evaluating whether the output is correct) do not. You can use Claude every day for months and still be bad at spotting when it's confidently wrong.

A TikTok creator named Logan ([@loganinthefuture](https://www.tiktok.com/@loganinthefuture)) put it more bluntly: "I did not go and put queries into Claude, because I know that is not enough to actually learn. That can be like 'spot learning.' But if you want to actually understand something, you need active learning mode, which involves a lot of friction."

The friction is the point. This system creates it.

## How it works

Three pieces that work together:

```
You close a session
  └── SessionEnd hook silently writes a learning note          ← capture

You come back after 5+ minutes
  └── Recap fires ("recap: we were building X...")
       └── CLAUDE.md rule suggests: "Run /learn?"              ← prompt

You run /learn
  └── Reads your accumulated learning notes
       ├── Identifies concepts you encountered
       ├── Connects them to things you already know (analogies)
       ├── Quizzes you (recall, not recognition)
       └── Saves results back to your notes                    ← friction
```

| Piece | What it solves | Without it |
|---|---|---|
| **SessionEnd hook** | Capture — nothing gets lost | You'd have to remember what happened last session |
| **CLAUDE.md rule** | Timing — surfaces learning at the natural breakpoint | You'd have to remember to invoke /learn |
| **/learn command** | Friction — active recall, not passive reading | You'd just skim a summary and forget it |

## Installation

### 1. Copy the command

```bash
cp commands/learn.md ~/.claude/commands/learn.md
```

### 2. Copy the capture script

```bash
mkdir -p ~/.claude/scripts
cp scripts/session-learn.py ~/.claude/scripts/session-learn.py
chmod +x ~/.claude/scripts/session-learn.py
```

By default, learning notes are written to `~/Documents/Obsidian Vault/Learning/`. To change this, set the `LEARN_NOTES_DIR` environment variable:

```bash
export LEARN_NOTES_DIR="$HOME/notes/learning"
```

### 3. Add the SessionEnd hook

Add this to your `~/.claude/settings.json` under `hooks.SessionEnd`:

```json
{
  "matcher": "",
  "hooks": [
    {
      "type": "command",
      "command": "python3 \"$HOME/.claude/scripts/session-learn.py\"",
      "timeout": 15
    }
  ]
}
```

### 4. Add the recap companion rule (optional)

Add this to your `CLAUDE.md` (global or project-level):

```markdown
### Active Learning
After generating a session recap (the "recap:" message shown when resuming after idle),
add one line: **"Run `/learn` to quiz yourself on what you just built."**
Keep it brief — don't push, just surface the option.
```

## What a /learn session looks like

```
You: /learn

Claude: This session covered 3 concepts worth quizzing on.

Concept 1: Hooks vs Skills

Think of a hook like a smoke detector — it fires automatically when
something happens, no one presses a button. A skill is like a recipe
book — Claude glances at it when the task seems relevant.

Question: We put the learning script on a SessionEnd hook instead of
making it a skill. Why would a skill have been the wrong choice?

You: Because skills are probabilistic — Claude might decide it's not
relevant and skip it. The hook fires every time, deterministically.

Claude: Exactly right. [adds depth, moves to next concept...]
```

After the quiz, results are saved to your learning notes folder with what you got right, what you missed, and when to review again.

## Design decisions

**Why a hook for capture, not a skill?** Hooks are deterministic — they fire every time. Skills are probabilistic — Claude decides if they're relevant. Capture needs to happen reliably, so it's a hook.

**Why a command for the quiz, not a hook?** The quiz is interactive — it needs to ask questions and wait for answers. Hooks run shell commands and can't have conversations. Commands are user-invoked and interactive.

**Why friction?** Research shows passive review (reading summaries, skimming notes) doesn't build durable understanding. Active recall — being asked a question and having to produce the answer — is what makes knowledge stick. The quiz is intentionally a little uncomfortable. That's the learning happening.

**Why analogies first?** Complex technical concepts land better when connected to something you already understand. "A hook is like a smoke detector" creates a mental anchor before "hooks are deterministic event handlers." The analogy gives you something to hang the technical definition on.

## Customization

### Learning notes directory

Set `LEARN_NOTES_DIR` to write notes anywhere:

```bash
export LEARN_NOTES_DIR="$HOME/my-notes/learning"
```

Works with Obsidian, plain markdown folders, or any note-taking system that reads `.md` files.

### Adapting the /learn command

The command in `commands/learn.md` is a prompt — edit it to match your learning style. You might want:
- More questions per session (change "2-3 questions max" to 5)
- Different note format
- Focus on specific domains (add "prioritize concepts related to X")

### Concept extraction

The capture script (`session-learn.py`) uses simple regex patterns to identify technical concepts. Add your own domain patterns to the `tech_patterns` list for better extraction in your field.

## Background

Built by a product manager learning software development with Claude Code. The insight came from noticing that weeks of productive sessions left surprisingly shallow understanding — I could build things but couldn't always explain why they worked. The system is designed for that gap.

## License

MIT
